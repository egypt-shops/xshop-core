from django.core.exceptions import ValidationError
from django.test import Client, TestCase, tag
from django.urls import reverse
from model_bakery import baker

from xshop.products.models import Product
from xshop.users.models import User


@tag("cartview")
class CartTests(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(
            User,
            mobile="01010101010",
            name="Hatem",
        )
        self.password = "testpass123"
        self.user.set_password(self.password)
        self.user.save()
        self.product = baker.make(Product, stock=10)
        self.payload = {"product_id": self.product.id, "quantity": 10, "actions": "add"}
        self.payload_remove = {"action": "remove", "productid": self.product.id}
        self.client = Client()
        self.url = reverse("cart:cart_ops")

    def test_get_cart_not_authenticated(self):
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 302)

    def test_get_cart(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(self.client.session.get("cart")), 0)

    def test_add_product_to_cart(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.post(self.url, data=self.payload)

        self.assertRedirects(
            resp,
            "/cart/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        self.assertNotEqual(len(self.client.session.get("cart")), 0)

    def test_add_none_existing_product_to_cart(self):
        self.payload["product_id"] = 100
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.post(self.url, data=self.payload)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(self.client.session.get("cart")), 0)
        self.assertRaisesMessage(ValidationError, "product_id", raise_exception=True)

    def test_update_product_in_cart(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        self.client.post(self.url, data=self.payload)
        self.payload["quantity"] = 3
        self.payload["actions"] = "update"
        resp = self.client.post(self.url, data=self.payload)
        user_cart = self.client.session.get("cart")

        self.assertRedirects(
            resp,
            "/cart/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        self.assertEqual(user_cart[str(self.product.id)]["quantity"], 3)

    def test_update_product_quantity_greater_than_stock(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        self.client.post(self.url, data=self.payload)
        self.payload["quantity"] = 123
        self.payload["actions"] = "update"
        resp = self.client.post(self.url, data=self.payload)
        user_cart = self.client.session.get("cart")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(user_cart[str(self.product.id)]["quantity"], 1)
        self.assertRaisesMessage(ValidationError, "quantity", raise_exception=True)

    def test_update_none_existing_product(self):
        self.payload["product_id"] = 3
        self.payload["actions"] = "update"
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.post(self.url, data=self.payload)

        self.assertEqual(resp.status_code, 200)
        self.assertRaisesMessage(ValidationError, "product_id", raise_exception=True)

    def test_remove_product_from_cart(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        self.client.post(self.url, data=self.payload)
        resp = self.client.post(self.url, data=self.payload_remove, xhr=True)

        self.assertRedirects(
            resp,
            "/cart/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        self.assertEqual(len(self.client.session.get("cart")), 0)

    def test_remove_none_existing_product_from_cart(self):
        self.payload_remove["productid"] = 1235
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.post(self.url, data=self.payload_remove, xhr=True)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(len(self.client.session.get("cart")), 0)
        self.assertRaisesMessage(ValidationError, "product_id", raise_exception=True)

    def test_clear_cart(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        self.client.post(self.url, data=self.payload, xhr=True)
        self.payload["action"] = "clear"
        resp = self.client.post(self.url, data=self.payload)

        self.assertRedirects(
            resp,
            "/cart/",
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
