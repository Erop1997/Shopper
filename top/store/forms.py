from django import forms
from .bulma_mixin import BulmaMixixn
from .models import *

# Узнать о Mixin, не работает с Textarea, потому что нет input_type

class OrderForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите адрес доставки', 'class':'input'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите номер телефона', 'class':'input'}))
    comments = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Добавьте комментарии к заказу', 'class':'textarea'}))
    status = forms.ChoiceField(choices=STATUS, required=True, label='Статус')

    class Meta():
        model = Order
        fields = ['address', 'phone','comments','status',]


class EditProfileForm(BulmaMixixn, forms.ModelForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    username = forms.CharField(label='Никнейм')
    email = forms.EmailField(label='Адрес Почты')

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']

class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class':'textarea'}),label = 'Можете оставить ваш отзыв здесь')
    rating = forms.ChoiceField(choices=RATE_CHOICES, required=True, label='Оцените продукт')

    class Meta:
        model = Review
        fields = ['text','rating']