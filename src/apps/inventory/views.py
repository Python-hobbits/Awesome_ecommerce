from django.views.generic import DetailView, ListView

from src.apps.inventory.models import Product, Category


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"
    slug_url_kwarg = "product_slug"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "category_detail.html"
    context_object_name = "category"
    slug_url_kwarg = "category_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(category=self.object)
        return context


class ProductBySellerListView(ListView):
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
