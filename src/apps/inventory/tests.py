from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from src.apps.inventory.models import Category, Product


class CategoryModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Test Category")

    def test_category_slug(self):
        self.assertEqual(self.category.slug, "test-category")

    # TODO uncomment when business requirements have somthing about category uniqueness

    # def test_duplicate_category_slug(self):
    #     with self.assertRaises(IntegrityError):
    #         Category.objects.create(name="Test Category")


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

    def test_nonexistent_category_detail_view(self):
        non_existent_slug = "non-existent-slug"
        url = reverse("category_detail", args=[non_existent_slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


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

    def test_nonexistent_product_detail_view(self):
        non_existent_category_slug = "non-existent-slug"
        non_existent_product_slug = "non-existent-product-slug"
        url = reverse(
            "product_detail", args=[non_existent_category_slug, non_existent_product_slug]
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_product_in_category_detail_view(self):
        non_existent_category_slug = "non-existent-slug"
        url = reverse("product_detail", args=[non_existent_category_slug, self.product.slug])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class ProductBySellerListViewTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser2", password="password", user_type="Seller"
        )
        self.url = reverse("product_by_seller")

    def test_authenticated_user_view(self):
        self.client.login(username="testuser2", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "product_by_seller_list.html")

    def test_unauthenticated_user_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class ProductCreateViewTestCase(TestCase):
    def setUp(self):
        self.user_seller = get_user_model().objects.create_user(
            username="seller", password="password", user_type="Seller"
        )
        self.user_buyer = get_user_model().objects.create_user(
            username="buyer", password="password", user_type="Buyer"
        )
        self.test_category = Category.objects.create(name="Test Category")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("product_create"))
        self.assertEqual(response.status_code, 302)  # Redirects to login page

    def test_redirect_if_not_seller(self):
        self.client.login(username="buyer", password="password")
        response = self.client.get(reverse("product_create"))
        self.assertEqual(response.status_code, 403)  # Forbidden access

    def test_access_for_seller(self):
        self.client.login(username="seller", password="password")
        response = self.client.get(reverse("product_create"))
        self.assertEqual(response.status_code, 200)

    def test_form_valid(self):
        self.client.login(username="seller", password="password")
        data = {
            "name": "Test Product",
            "description": "This is a test product",
            "category": self.test_category.id,
            "price": 10.99,
        }
        response = self.client.post(reverse("product_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name="Test Product").exists())

    def test_form_invalid(self):
        self.client.login(username="seller", password="password")
        data = {}  # Missing required form fields
        response = self.client.post(reverse("product_create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Product.objects.filter(name="Test Product").exists())
