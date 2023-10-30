from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from src.apps.inventory.models import Product
from src.apps.basket.basket import Basket
from src.apps.basket.forms import BasketAddProductForm


def basket_add(request, product_id):
    """
    This view function is responsible for adding a product to the user's basket.
    It handles the form submission, validates the form data, and checks product
    availability in stock before adding it to the basket.

    -If the product is successfully added to the basket, a success message is
    displayed to the user.
    -If the quantity exceeds the available stock, an error message is shown.
    -Redirects the user back to the previous page.
    """
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    form = BasketAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data

        quantity_in_basket = basket.get_quantity(product)
        total_quantity = quantity_in_basket + cd["quantity"]

        if product.stock < cd["quantity"] or product.stock < total_quantity:
            messages.error(
                request,
                f"Insufficient quantity of goods in stock. Available {product.stock}."
                f" You have already added {basket.get_quantity(product)}",
            )
        else:
            basket.add(product=product, quantity=cd["quantity"], update_quantity=cd["update"])
            messages.success(request, f"Product {product.name} successfully added to cart.")
            basket.save()
    return redirect(request.META.get("HTTP_REFERER"))


def basket_remove(request, product_id):
    """
    This view function handles the removal of a specific product from
    the user's basket. It utilizes the Basket class to remove the product
    and then redirects the user to the basket detail page.
    """
    basket = Basket(request)
    product = get_object_or_404(Product, id=product_id)
    basket.remove(product)
    return redirect("basket:basket_detail")


def basket_detail(request):
    """
    This view function renders the user's basket content using the
    "basket/basket_detail.html" template. The basket contents are
    passed to the template for display.
    """
    basket = Basket(request)
    return render(request, "basket/basket_detail.html", {"basket": basket})
