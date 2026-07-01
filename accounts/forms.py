from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, label='Роль')

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')
        labels = {
            'username': 'Логін',
            'email': 'Електронна пошта',
        }
        help_texts = {
            'username': '',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'username': 'Ваш логін',
            'email': 'you@example.com',
            'password1': 'Пароль',
            'password2': 'Повторіть пароль',
        }
        for name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')
            if name in placeholders:
                field.widget.attrs.setdefault('placeholder', placeholders[name])


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логін')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ваш логін',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ваш пароль',
        })
