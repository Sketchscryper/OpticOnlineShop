from __future__ import annotations

import time

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import CheckoutForm


@login_required
def checkout(request: HttpRequest) -> HttpResponse:
    # Redirect back if cart is empty
    cart: dict[str, int] | None = request.session.get("cart")  # from cart app
    if not cart or not any(int(q or 0) > 0 for q in cart.values()):
        messages.info(request, "Корзина пуста. Добавьте товары перед оформлением заказа.")
        return redirect(reverse("cart:detail"))

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Imitate order creation: generate a fake order id
            fake_order_id = int(time.time())
            # Clear cart
            request.session["cart"] = {}
            request.session.modified = True
            messages.success(request, "Заказ успешно оформлен!")
            return redirect(reverse("orders:success", kwargs={"order_id": fake_order_id}))
    else:
        initial = {
            "full_name": getattr(request.user, "get_full_name", lambda: "")() or request.user.username,
            "email": getattr(request.user, "email", "") or "",
        }
        form = CheckoutForm(initial=initial)

    return render(request, "orders/checkout.html", {"form": form})


@login_required
def order_success(request: HttpRequest, order_id: int) -> HttpResponse:
    return render(request, "orders/success.html", {"order_id": order_id})
