from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import OrderForm
from .models import Order, OrderItem
from cart.cart import Cart

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Корзина пуста")
        return redirect('catalog:product_list')

    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            # Проверка остатков
            stock_errors = []
            for item in cart:
                product = item['product']
                if item['quantity'] > product.stock:
                    stock_errors.append(f"{product.name}: доступно {product.stock}, вы заказали {item['quantity']}")
            
            if stock_errors:
                for error in stock_errors:
                    messages.error(request, error)
                return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})
            
            # Создание заказа
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            
            # Создание позиций и уменьшение остатков
            for item in cart:
                product = item['product']
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=product.price,
                    quantity=item['quantity']
                )
                product.stock -= item['quantity']
                product.save()
            
            cart.clear()
            messages.success(request, f"Заказ №{order.id} успешно оформлен!")
            return redirect('orders:order_success', order_id=order.id)
    else:
        initial = {}
        if hasattr(request.user, 'profile'):
            profile = request.user.profile
            initial = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'phone': profile.phone,
                'email': request.user.email,
                'address': profile.address,
            }
        form = OrderForm(user=request.user, initial=initial)
    
    return render(request, 'orders/checkout.html', {'form': form, 'cart': cart})

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/success.html', {'order': order})
