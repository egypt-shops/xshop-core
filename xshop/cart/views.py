from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from xshop.cart.cart import Cart
from xshop.cart.forms import CartPostProductForm
from xshop.products.models import Product
from xshop.products.api.serializers import ProductSerializer


class CartView(LoginRequiredMixin, ListView):
    def post(self, request):  # class based view def post, def get
        cart = Cart(request)
        form = CartPostProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            quantity = int(cd["quantity"])
            action = cd["actions"]
            product = cd["product"]

            # if action == "add":
            #     cart.add(product=product)

            #     return redirect("cart:cart_ops")

            if action == "update":
                cart.update(
                    product=product,
                    quantity=quantity,
                )

                return redirect("cart:cart_ops")

        if request.POST.get("actions") == "add":
            product_id = int(request.POST.get("product_id"))
            try:
                product = Product.objects.get(id=product_id)

                product_json = ProductSerializer(product).data

                cart.add(product=product_json)

                return redirect("cart:cart_ops")
            except Product.DoesNotExist:
                form.errors["product_id"] = "Not found"

        if request.POST.get("action") == "remove":
            product_id = int(request.POST.get("productid"))
            cart.remove(product_id)
            return redirect("cart:cart_ops")

        if request.POST.get("action") == "clear":
            cart.clear()

            return redirect("cart:cart_ops")

        full_price = 0
        for item in cart:
            full_price += item["total_price"]
            item["update_quantity_form"] = CartPostProductForm(
                initial={
                    "quantity": item["quantity"],
                    "actions": "update",
                    "product_id": item["product"]["id"],
                }
            )
        context = {
            "cart": cart,
            "full_price": full_price,
            "user": request.user,
            "errors": form.errors,
        }
        return render(request, "pages/cart.html", context)

    def get(self, request):
        cart = Cart(request)
        full_price = 0
        for item in cart:
            full_price += item["total_price"]
            item["update_quantity_form"] = CartPostProductForm(
                initial={
                    "quantity": item["quantity"],
                    "actions": "update",
                    "product_id": item["product"]["id"],
                }
            )
        context = {
            "cart": cart,
            "full_price": full_price,
            "user": request.user,
        }
        return render(request, "pages/cart.html", context)
