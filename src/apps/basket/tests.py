from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages


from src.apps.basket.basket import Basket
from src.apps.inventory.models import Product, Category


class BasketAddViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.user_seller = get_user_model().objects.create_user(
            username="seller", password="password", user_type="Seller"
        )
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=10.0,
            seller=self.user_seller,
            stock=10,
        )

    def test_add_product_to_basket(self):
        self.client.login(username="testuser", password="testpassword")
        basket = Basket(self.client)
        initial_quantity = basket.get_quantity(self.product)
        response = self.client.post(
            reverse("basket:basket_add", args=[self.product.id]),
            {"quantity": 5, "update": False},
            HTTP_REFERER="/",
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(str(messages[0]).startswith(f"Product {self.product.name}"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Basket(self.client).get_quantity(self.product), initial_quantity + 5)

    def test_add_product_to_basket_insufficient_stock(self):
        self.client.login(username="testuser", password="testpassword")
        basket = Basket(self.client)
        initial_quantity = basket.get_quantity(self.product)
        response = self.client.post(
            reverse("basket:basket_add", args=[self.product.id]),
            {"quantity": 11, "update": False},
            HTTP_REFERER="/",
        )
        messages = list(get_messages(response.wsgi_request))

        self.assertTrue(str(messages[0]).startswith("Insufficient quantity"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Basket(self.client).get_quantity(self.product), initial_quantity)


class BasketRemoveViewTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.user_seller = get_user_model().objects.create_user(
            username="seller", password="password", user_type="Seller"
        )
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=10.0,
            seller=self.user_seller,
            stock=10,
        )

    def test_remove_product_from_basket(self):
        self.client.login(username="testuser", password="testpassword")
        self.client.post(
            reverse("basket:basket_add", args=[self.product.id]),
            {"quantity": 5, "update": False},
            HTTP_REFERER="/",
        )
        response = self.client.get(reverse("basket:basket_remove", args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session["basket"], {})


class BasketDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="password")

    def test_display_basket_contents(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("basket:basket_detail"))
        self.assertEqual(response.status_code, 200)
