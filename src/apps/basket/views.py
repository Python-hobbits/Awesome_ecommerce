from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from src.apps.inventory.models import Product
from src.apps.basket.basket import Basket
from src.apps.basket.forms import BasketAddProductForm


def basket_add(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    form = BasketAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data

        quantity_in_basket = basket.get_quantity(product)
        total_quantity = quantity_in_basket + cd["quantity"]

        if product.stock < cd["quantity"] or product.stock < total_quantity:
            messages.error(
                request, f"Insufficient quantity of goods in stock. Available {product.stock}"
            )
        else:
            basket.add(product=product, quantity=cd["quantity"], update_quantity=cd["update"])
            messages.success(request, f"Product {product.name} successfully added to cart.")

    return redirect(request.META.get("HTTP_REFERER"))


def basket_remove(request, product_id):
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    basket.remove(product)
    return redirect("basket:basket_detail")


def basket_detail(request):
    basket = Basket(request)
    return render(request, "basket/basket_detail.html", {"basket": basket})
