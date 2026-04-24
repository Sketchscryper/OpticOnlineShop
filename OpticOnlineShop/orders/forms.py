from django import forms
from .models import Order
import re

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'email', 'address', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        digits = re.sub(r'\D', '', phone)
        if len(digits) != 11:
            raise forms.ValidationError("Номер телефона должен содержать 11 цифр.")
        if not (digits.startswith('7') or digits.startswith('8')):
            raise forms.ValidationError("Номер должен начинаться с +7 или 8.")
        if digits.startswith('8'):
            digits = '7' + digits[1:]
        return f"+{digits}"