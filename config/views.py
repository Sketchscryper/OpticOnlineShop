from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView


class RegisterForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        labels = {
            'username': 'Логин',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('catalog:product_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Регистрация прошла успешно. Добро пожаловать!')
        return response
