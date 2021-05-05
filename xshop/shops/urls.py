from django.urls import path

from . import views

app_name = "shop"

urlpatterns = [
    path("<int:shop_id>", views.ShopDetailView.as_view(), name="shop_details"),
]
