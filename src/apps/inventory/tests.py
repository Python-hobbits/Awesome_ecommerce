from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from src.apps.inventory.models import Category, Product


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_category_slug(self):
        self.assertEqual(self.category.slug, "test-category")


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.user = get_user_model().objects.create_user(username="testuser", password="password")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=10.0,
            seller=self.user,
        )

    def test_product_slug(self):
        self.assertEqual(self.product.slug, "test-product")

    def test_product_absolute_url(self):
        expected_url = reverse("product_detail", args=[self.category.slug, self.product.slug])
        self.assertEqual(self.product.get_absolute_url(), expected_url)


class CategoryDetailViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.url = reverse("category_detail", args=[self.category.slug])

    def test_category_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "category_detail.html")


class ProductDetailViewTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")
        self.user = get_user_model().objects.create_user(username="testuser", password="password")
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
            price=10.0,
            seller=self.user,
        )
        self.url = reverse("product_detail", args=[self.category.slug, self.product.slug])

    def test_product_detail_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_detail.html")


class ProductBySellerListViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser2", password="password")
        self.url = reverse("product_by_seller")

    def test_authenticated_user_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_list.html")
