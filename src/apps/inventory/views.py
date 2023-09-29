from django.views.generic import DetailView, ListView

from src.apps.inventory.models import Product


class ProductDetailView(DetailView):
    model = Product


class ProductBySellerListView(ListView):
    model = Product
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Product.objects.filter(seller=self.request.user)
        else:
            return Product.objects.none()
