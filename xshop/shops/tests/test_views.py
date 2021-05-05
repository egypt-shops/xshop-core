from django.test import Client, TestCase, tag
from django.urls import reverse
from model_bakery import baker
from rest_framework import status

from xshop.shops.models import Shop
from xshop.users.models import User
from xshop.products.models import Product


@tag("shopdetailview")
class ShopDetailViewTests(TestCase):
    def setUp(self) -> None:
        self.user = baker.make(
            User,
            mobile="01010101010",
            name="Hatem",
        )
        self.password = "testpass123"
        self.user.set_password(self.password)
        self.user.save()
        self.shop = baker.make(Shop, mobile="01222222222")
        self.product = baker.make(Product, shop=self.shop)
        self.client = Client()
        self.url = reverse("shop:shop_details", kwargs={"shop_id": self.shop.id})

    def test_get_shop_details_not_authenticated(self):
        resp = self.client.get(self.url)

        self.assertRedirects(
            resp,
            "/users/login/?next=/shop/{}".format(self.shop.id),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_get_shop_details(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "pages/shop_details.html")

    def test_retreive_products(self):
        self.client.login(mobile=self.user.mobile, password=self.password)
        resp = self.client.get("/shop/{}".format(self.shop.id))
        self.assertEqual(len(resp.context["products"]), 1)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
