from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, Order


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ім\'я'
    }))
    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Прізвище'
    }))
    phone = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': '+38 (XXX) XXX-XX-XX'
    }))
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Підтвердіть пароль'
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Цей email уже зареєстрований')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomerRegistrationForm(UserRegistrationForm):
    pass


class DriverRegistrationForm(UserRegistrationForm):
    license_number = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Номер водійського посвідчення'
    }))
    experience_years = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Років досвіду'
    }))


class AdminRegistrationForm(UserRegistrationForm):
    admin_code = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Адмін-код'
    }))


class OrderForm(forms.ModelForm):
    pickup_location = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Точка відправлення'
    }))
    dropoff_location = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Куди поїхати'
    }))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Додаткова інформація (опціонально)',
        'rows': 3
    }))
    
    class Meta:
        model = Order
        fields = ['pickup_location', 'dropoff_location', 'service_type', 'notes']
        widgets = {
            'service_type': forms.Select(attrs={
                'class': 'form-control'
            })
        }
