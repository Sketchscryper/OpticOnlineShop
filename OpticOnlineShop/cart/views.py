from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from catalog.models import Product
from .cart import Cart

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > product.stock:
        messages.error(request, f"Доступно только {product.stock} шт. товара {product.name}")
        return redirect('catalog:product_detail', slug=product.slug)
    
    cart.add(product=product, quantity=quantity)
    messages.success(request, f"{product.name} добавлен в корзину")
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, "Товар удалён из корзины")
    return redirect('cart:cart_detail')

def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id, is_active=True)
    quantity = int(request.POST.get('quantity', 0))
    
    if quantity > product.stock:
        messages.error(request, f"Доступно только {product.stock} шт. товара {product.name}")
    elif quantity > 0:
        cart.add(product=product, quantity=quantity, override_quantity=True)
        messages.success(request, "Корзина обновлена")
    else:
        cart.remove(product)
    
    return redirect('cart:cart_detail')
