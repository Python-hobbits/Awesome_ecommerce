from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView

from src.apps.basket.basket import Basket
from .forms import DeliveryOptionForm
from .models import Order, OrderProduct


class CheckoutView(LoginRequiredMixin, View):
    template_name = "orders/checkout.html"

    def get(self, request, *args, **kwargs):
        basket = Basket(request)
        total_price = basket.get_total_price()
        delivery_option_form = DeliveryOptionForm()

        return render(
            request,
            self.template_name,
            {
                "basket": basket,
                "total_price": total_price,
                "delivery_option_form": delivery_option_form,
            },
        )

    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        total_price = basket.get_total_price()
        delivery_option_form = DeliveryOptionForm(request.POST)

        if delivery_option_form.is_valid():
            order = Order.objects.create(
                user_id=request.user,
                user_name=request.user.first_name,
                user_email=request.user.email,
            )

            for item in basket:
                product = item["product"]
                quantity = item["quantity"]
                price = item["price"]
                OrderProduct.objects.create(
                    order=order, product_id=product, quantity=quantity, product_price=price
                )

            delivery_method = delivery_option_form.save(commit=False)
            delivery_method.order = order
            delivery_method.save()

            basket.clear()

            return HttpResponseRedirect(reverse("thank_you", kwargs={"order_id": order.id}))

        return render(
            request,
            self.template_name,
            {
                "basket": basket,
                "total_price": total_price,
                "delivery_option_form": delivery_option_form,
            },
        )


class ThankYouView(UserPassesTestMixin, DetailView):
    model = Order
    template_name = "orders/thank_you.html"
    context_object_name = "order"
    pk_url_kwarg = "order_id"

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.user_id

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        total_price = sum(
            order_product.get_total_price() for order_product in order.orderproduct_set.all()
        )

        context = {"order": order, "total_price": total_price}
        return render(request, self.template_name, context)
