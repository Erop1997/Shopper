from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .bulma_mixin import BulmaMixixn

class RegistrationForm(BulmaMixixn, UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите ваше имя'}),label='Ваше имя')
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Придумайте никнейм'}),label='Придумайте никнейм')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Придумайте пароль'}),label='Придумайте пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Повторите пароль'}),label='Введите пароль повторно')
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder':'Введите адрес электронной почты'}),label='Введите ваш E-mail')

    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']

class LoginForm(BulmaMixixn, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Введите никнейм'}),label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Введите пароль'}),label='Пароль')
    
    class Meta:
        model = User
        fields = ['username', 'password']