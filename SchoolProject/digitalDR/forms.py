from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Логин'}))
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={'type': 'password', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
