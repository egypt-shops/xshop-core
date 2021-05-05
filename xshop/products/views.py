from django.views.generic import TemplateView
from django.shortcuts import render
from xshop.products.models import Product
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductDetailView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        product_id = kwargs["product_id"]
        product = Product.objects.get(id=product_id)
        price = str(product.price)[4:]
        context = {
            "product": product,
            "price": price,
        }
        return render(request, "pages/product_detail.html", context)
