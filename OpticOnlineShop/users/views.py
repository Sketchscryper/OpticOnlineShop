from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
from .models import UserProfile
from orders.models import Order

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация прошла успешно! Добро пожаловать!")
            return redirect('users:profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-created')
    orders_count = orders.count()
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    context = {
        'user': user,
        'profile': profile,
        'orders': orders[:10],
        'orders_count': orders_count,
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.email = request.POST.get('email')
            user.save()
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, "Профиль успешно обновлён!")
            return redirect('users:profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        initial_data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'phone': profile.phone,
            'address': profile.address,
        }
        form = UserProfileForm(initial=initial_data, instance=profile)
    
    return render(request, 'users/profile_edit.html', {'form': form, 'user': user})
