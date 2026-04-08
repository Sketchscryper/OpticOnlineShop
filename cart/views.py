from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from catalog.models import Product


SESSION_KEY = "cart"


@dataclass(frozen=True)
class CartLine:
    product: Product
    quantity: int

    @property
    def line_total(self) -> Decimal:
        return self.product.price * self.quantity


def _get_cart_dict(session) -> dict[str, int]:
    cart = session.get(SESSION_KEY)
    if not isinstance(cart, dict):
        cart = {}
        session[SESSION_KEY] = cart
    return cart


def _cart_lines(request: HttpRequest) -> list[CartLine]:
    cart = _get_cart_dict(request.session)
    ids = [int(pid) for pid in cart.keys() if str(pid).isdigit()]
    products = Product.objects.filter(id__in=ids, is_active=True).select_related("category")
    products_by_id = {p.id: p for p in products}

    lines: list[CartLine] = []
    for pid_str, qty in cart.items():
        try:
            pid = int(pid_str)
        except ValueError:
            continue
        product = products_by_id.get(pid)
        if not product:
            continue
        try:
            quantity = int(qty)
        except (TypeError, ValueError):
            quantity = 0
        if quantity > 0:
            lines.append(CartLine(product=product, quantity=quantity))
    return lines


def cart_detail(request: HttpRequest) -> HttpResponse:
    lines = _cart_lines(request)
    total = sum((line.line_total for line in lines), Decimal("0.00"))
    items_count = sum((line.quantity for line in lines), 0)
    return render(
        request,
        "cart/detail.html",
        {"lines": lines, "total": total, "items_count": items_count},
    )


@require_POST
def cart_add(request: HttpRequest, product_id: int) -> HttpResponse:
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity_raw = request.POST.get("quantity", "1")
    try:
        quantity = max(1, min(99, int(quantity_raw)))
    except ValueError:
        quantity = 1

    cart = _get_cart_dict(request.session)
    key = str(product.id)
    cart[key] = int(cart.get(key, 0)) + quantity
    request.session.modified = True

    messages.success(request, f"Добавлено в корзину: {product.name}")
    return redirect(product.get_absolute_url())


@require_POST
def cart_remove(request: HttpRequest, product_id: int) -> HttpResponse:
    cart = _get_cart_dict(request.session)
    cart.pop(str(product_id), None)
    request.session.modified = True
    messages.info(request, "Товар удалён из корзины")
    return redirect(reverse("cart:detail"))


@require_POST
def cart_update(request: HttpRequest, product_id: int) -> HttpResponse:
    quantity_raw = request.POST.get("quantity", "1")
    try:
        quantity = max(0, min(99, int(quantity_raw)))
    except ValueError:
        quantity = 1

    cart = _get_cart_dict(request.session)
    key = str(product_id)
    if quantity <= 0:
        cart.pop(key, None)
    else:
        cart[key] = quantity
    request.session.modified = True
    messages.success(request, "Корзина обновлена")
    return redirect(reverse("cart:detail"))
