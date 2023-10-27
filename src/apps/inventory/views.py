from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django_filters import FilterSet, CharFilter, ModelChoiceFilter, BooleanFilter

from src.apps.inventory.forms import ProductForm, ProductImageForm
from src.apps.inventory.models import Product, Category, ProductImage


class ProductDetailView(DetailView):
    """
    This class-based view displays detailed information about a product,
    including its name, description, and price.
    """

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "product_slug"

    def get_queryset(self):
        """
        Get a filtered queryset of products based on the associated category.
        """
        category_slug = self.kwargs.get("category_slug")
        category = get_object_or_404(Category, slug=category_slug)
        queryset = Product.objects.filter(category=category, is_active=True)
        return queryset

    def get(self, request, *args, **kwargs):
        """
        Checks the stock availability of the product. If the product is out of stock,
        an "Out of stock" message is displayed to the user.
        """
        product = self.get_object()
        if product.stock == 0:
            messages.error(self.request, "Out of stock")
        return super().get(request, *args, **kwargs)


class ProductFilter(FilterSet):
    """
    This FilterSet is used for filtering and searching products.
    It provides filters for product name, category, and stock availability.
    Additionally, it allows filtering products based on price
    (less than or greater than).
    """

    name = CharFilter(field_name="name", lookup_expr="icontains", label="Name contains")
    category = ModelChoiceFilter(
        field_name="category", queryset=Category.objects.all(), label="Category"
    )
    in_stock = BooleanFilter(field_name="in_stock", label="In Stock")

    class Meta:
        model = Product
        fields = {
            "price": ["lt", "gt"],
        }


# TODO: refactor this mess so that seller could filter products by stock availability

# class CustomBooleanFilter(django_filters.BooleanFilter):
#     def filter(self, queryset, value):
#         if value is True:
#             return queryset.exclude(**{self.field_name: 0})
#         elif value is None:
#             return queryset
#         return queryset.filter(**{self.field_name: 0})
#
#
# class SellerProductFilter(ProductFilter):
#     stock = CustomBooleanFilter(field_name="stock", label="Stock (In Stock)")


class ProductIsActiveFilter(FilterSet):
    is_active = BooleanFilter(field_name="is_active", label="Is Active")


class BaseProductListView(ListView):
    model = Product
    paginate_by = 10
    filterset_class = ProductFilter
    context_object_name = "products"

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET:
            queryset = self.filterset_class(self.request.GET, queryset=queryset).qs
        return queryset

    def get_ordering(self):
        order_by = self.request.GET.get("order_by")
        allowed_ordering_fields = ["name", "-name", "price", "-price"]

        if order_by in allowed_ordering_fields:
            return (order_by,)
        return ("-price",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset_class(self.request.GET)
        return context


class ProductListView(BaseProductListView):
    template_name = "product_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_active=True)


class CategoryDetailView(BaseProductListView):
    template_name = "category_detail.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs["category_slug"]
        category = get_object_or_404(Category, slug=category_slug)
        return queryset.filter(category=category, stock__gt=0)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs["category_slug"]
        context["category"] = get_object_or_404(Category, slug=category_slug)
        return context


class ProductBySellerListView(LoginRequiredMixin, BaseProductListView):
    template_name = "product_by_seller_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = ProductIsActiveFilter(self.request.GET, queryset=queryset).qs
        return queryset.filter(seller=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_filter"] = ProductIsActiveFilter(
            self.request.GET, queryset=self.get_queryset(), request=self.request
        )
        return context


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_create.html"
    success_url = reverse_lazy("product_by_seller")

    def form_valid(self, form):
        form.instance.seller = self.request.user
        response = super().form_valid(form)

        images_form = ProductImageForm(self.request.POST, self.request.FILES)
        if images_form.is_valid():
            for image in self.request.FILES.getlist("image"):
                ProductImage.objects.create(product=self.object, image=image)

        return response

    def test_func(self):
        return self.request.user.user_type == "Seller"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images_form"] = ProductImageForm()
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView, UserPassesTestMixin):
    model = Product
    form_class = ProductForm
    template_name = "product_edit.html"
    success_url = reverse_lazy("product_by_seller")
    slug_url_kwarg = "product_slug"

    def form_valid(self, form):
        response = super().form_valid(form)
        ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=1)
        formset = ImageFormSet(
            self.request.POST, self.request.FILES, queryset=self.object.images.all()
        )

        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.product = self.object
                instance.save()

                if not instance.is_active:
                    instance.deactivated_at = timezone.now()
                else:
                    instance.deactivated_at = None
                instance.save()

        return response

    def test_func(self):
        return (
            self.request.user.user_type == "Seller"
            and self.request.user == self.get_object().seller
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ImageFormSet = modelformset_factory(ProductImage, form=ProductImageForm, extra=1)
        context["formset"] = ImageFormSet(queryset=ProductImage.objects.filter(product=self.object))
        return context


class ProductDeleteView(LoginRequiredMixin, DeleteView, UserPassesTestMixin):
    model = Product
    success_url = reverse_lazy("product_by_seller")
    slug_url_kwarg = "product_slug"
    template_name = "product_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        return result

    def test_func(self):
        return (
            self.request.user.user_type == "Seller"
            and self.request.user == self.get_object().seller
        )
