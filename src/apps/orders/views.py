from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import DeliveryOptionForm
from .models import Order, OrderProduct
from src.apps.basket.basket import Basket


class CheckoutView(View):
    template_name = 'orders/checkout.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            basket = Basket(request)
            total_price = basket.get_total_price()
            delivery_option_form = DeliveryOptionForm()
            return render(request, self.template_name, {'basket': basket, 'total_price': total_price, 'delivery_option_form': delivery_option_form})

        else:
            return HttpResponseRedirect(reverse('account_login'))

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
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
                    product = item['product']
                    quantity = item['quantity']
                    price = item['price']
                    OrderProduct.objects.create(order=order, product_id=product, quantity=quantity, product_price=price)

                delivery_method = delivery_option_form.save(commit=False)
                delivery_method.order = order
                delivery_method.save()

                basket.clear()

                return HttpResponseRedirect(reverse('thank_you', kwargs={'order_id': order.id}))

            return render(request, self.template_name, {'basket': basket, 'total_price': total_price, 'delivery_option_form': delivery_option_form})

        else:
            return HttpResponseRedirect(reverse('account_login'))


class ThankYouView(UserPassesTestMixin, View):
    template_name = 'orders/thank_you.html'

    def test_func(self):
        order = self.get_order()
        return self.request.user == order.user_id

    def get_order(self):
        order_id = self.kwargs['order_id']
        return get_object_or_404(Order, id=order_id)

    def get(self, request, *args, **kwargs):
        total_price = 0

        order = self.get_order()

        for order_product in order.orderproduct_set.all():
            total_price += order_product.get_total_price()

        context = {'order': order, 'total_price': total_price}
        return render(request, self.template_name, context)
