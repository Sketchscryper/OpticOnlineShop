from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        label="ФИО",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Иванов Иван Иванович"}),
    )
    phone = forms.CharField(
        label="Телефон",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "+7 900 000-00-00"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "name@example.com"}),
    )

    city = forms.CharField(
        label="Город",
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Москва"}),
    )
    street = forms.CharField(
        label="Улица",
        max_length=120,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Тверская"}),
    )
    house = forms.CharField(
        label="Дом/корпус",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "10к2"}),
    )
    apartment = forms.CharField(
        label="Квартира/офис",
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "15"}),
    )
    postal_code = forms.CharField(
        label="Почтовый индекс",
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "101000"}),
    )

    comment = forms.CharField(
        label="Комментарий к заказу",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Пожелания по доставке"}),
    )

