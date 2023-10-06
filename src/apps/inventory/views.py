from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView

from src.apps.inventory.forms import ProductForm, ProductFilterForm
from src.apps.inventory.models import Product, Category


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "product_slug"

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        category = get_object_or_404(Category, slug=category_slug)
        queryset = Product.objects.filter(category=category)
        return queryset


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category_detail.html"
    context_object_name = "category"
    slug_url_kwarg = "category_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(category=self.object)
        return context


class ProductBySellerListView(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 10
    template_name = "product_list.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Product.objects.filter(seller=self.request.user)
        return Product.objects.none()


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "products"
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.request.GET:
            filter_form = ProductFilterForm(self.request.GET)
            if filter_form.is_valid():
                name_query = filter_form.cleaned_data.get("name")
                if name_query:
                    queryset = queryset.filter(name__icontains=name_query)
                category = filter_form.cleaned_data.get("category")
                if category:
                    queryset = queryset.filter(category=category)
                min_price = filter_form.cleaned_data.get("min_price")
                max_price = filter_form.cleaned_data.get("max_price")
                if min_price is not None and max_price is not None:
                    queryset = queryset.filter(price__range=(min_price, max_price))

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = ProductFilterForm(self.request.GET)
        return context


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_create.html"
    success_url = reverse_lazy(
        "product_by_seller"
    )  # Redirect to a success URL (change this to your desired URL)

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.user_type == "Seller"
