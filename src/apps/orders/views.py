from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView

from src.apps.basket.basket import Basket
from .forms import DeliveryOptionForm, PaymentMethodForm
from .models import Order, OrderProduct


class CheckoutView(LoginRequiredMixin, View):
    template_name = "orders/checkout.html"
    product_list_url = reverse_lazy("product_list")

    def get(self, request, *args, **kwargs):
        basket = Basket(request)

        if not basket:
            return HttpResponseRedirect(self.product_list_url)

        total_price = basket.get_total_price()
        delivery_option_form = DeliveryOptionForm()
        payment_method_form = PaymentMethodForm()

        return render(
            request,
            self.template_name,
            {
                "basket": basket,
                "total_price": total_price,
                "delivery_option_form": delivery_option_form,
                "payment_method_form": payment_method_form,
            },
        )

    def post(self, request, *args, **kwargs):
        basket = Basket(request)
        total_price = basket.get_total_price()
        delivery_option_form = DeliveryOptionForm(request.POST)
        payment_method_form = PaymentMethodForm(request.POST)

        if not basket:
            return HttpResponseRedirect(self.product_list_url)

        if delivery_option_form.is_valid() and payment_method_form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    user_id=request.user,
                    user_name=request.user.first_name,
                    user_email=request.user.email,
                )

                order_products = []
                for item in basket:
                    product = item["product"]
                    quantity = item["quantity"]
                    price = item["price"]
                    order_products.append(
                        OrderProduct(
                            order=order, product_id=product, quantity=quantity, product_price=price
                        )
                    )

                OrderProduct.objects.bulk_create(order_products)

                delivery_method = delivery_option_form.save(commit=False)
                delivery_method.order = order
                delivery_method.save()

                payment_method = payment_method_form.save(commit=False)
                payment_method.order = order
                payment_method.save()

                basket.clear()

                return HttpResponseRedirect(reverse("thank_you", kwargs={"order_id": order.id}))

        return render(
            request,
            self.template_name,
            {
                "basket": basket,
                "total_price": total_price,
                "delivery_option_form": delivery_option_form,
                "payment_method_form": payment_method_form,
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

        delivery_method = order.deliveryoption_set.first()
        payment_method = order.paymentmethod_set.first()

        context = {
            "order": order,
            "total_price": total_price,
            "payment_method": payment_method.payment_method if payment_method else None,
            "delivery_method": delivery_method.delivery_method if delivery_method else None,
            "shipment_address": delivery_method.shipment_address if delivery_method else None,
        }

        return render(request, self.template_name, context)
