from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from src.apps.inventory.models import Product, Category

from src.apps.inventory.models import Product, Category
from django.db.models import Q

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
    paginate_by = 10
    template_name = "product_list.html"


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'inventory/categories_list.html'


class ProductsByCategoryListView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'inventory/products_by_category_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs['pk'])
        context['category'] = category
        return context


class ProductsListView(ListView):
    model = Product
    template_name = "inventory/search_category.html"
    context_object_name = 'products'



