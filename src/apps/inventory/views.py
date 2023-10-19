from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django_filters import FilterSet, CharFilter, ModelChoiceFilter

from src.apps.inventory.forms import ProductForm, ProductImageForm
from src.apps.inventory.models import Product, Category, ProductImage


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "product_slug"

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        category = get_object_or_404(Category, slug=category_slug)
        queryset = Product.objects.filter(category=category, is_active=True, stock__gt=0)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = self.object.images.filter(is_active=True)
        context["product_images"] = images
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category_detail.html"
    context_object_name = "category"
    slug_url_kwarg = "category_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(category=self.object)
        return context


class ProductFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="icontains", label="Name contains")
    category = ModelChoiceFilter(
        field_name="category", queryset=Category.objects.all(), label="Category"
    )

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
#


class ProductBySellerListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 10
    template_name = "product_by_seller_list.html"
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filterset_class(self.request.GET, queryset=queryset).qs
        return queryset.filter(seller=self.request.user, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset_class(self.request.GET)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_image"] = ProductImage.objects.filter(is_active=True).first()
        return context


class DeactivatedProductBySellerListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 10
    template_name = "product_by_seller_list.html"
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = self.filterset_class(self.request.GET, queryset=queryset).qs
        return queryset.filter(seller=self.request.user, is_active=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset_class(self.request.GET)
        return context


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"
    filterset_class = ProductFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.GET:
            queryset = self.filterset_class(self.request.GET, queryset=queryset).qs
        return queryset.filter(is_active=True, stock__gt=0)

    def get_ordering(self):
        order_by = self.request.GET.get("order_by")
        allowed_ordering_fields = ["name", "-name", "price", "-price"]

        if order_by in allowed_ordering_fields:
            return (order_by,)
        return ("-price",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter"] = self.filterset_class(self.request.GET)
        context["product_image"] = ProductImage.objects.filter(is_active=True).first()
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
