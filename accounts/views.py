from django.contrib.auth import login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm
from .models import User


ROLE_TITLES = {
    User.ROLE_CLIENT: {
        'title': 'Реєстрація клієнта',
        'subtitle': 'Створіть акаунт, щоб швидко замовляти поїздки та доставку.',
        'button': 'Зареєструватися як клієнт',
    },
    User.ROLE_DRIVER: {
        'title': 'Реєстрація водія',
        'subtitle': 'Приєднайтеся до команди Wheels Up і приймайте замовлення.',
        'button': 'Зареєструватися як водій',
    },
    User.ROLE_MANAGER: {
        'title': 'Реєстрація адміністратора',
        'subtitle': 'Створіть акаунт для керування замовленнями та командою.',
        'button': 'Зареєструватися як адміністратор',
    },
}


def register_view(request, template_name='register/register.html', role=None):
    if request.method == 'POST':
        data = request.POST.copy()
        if role:
            data['role'] = role
        form = RegisterForm(data)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm(initial={'role': role} if role else None)

    role_content = ROLE_TITLES.get(role, {
        'title': 'Реєстрація',
        'subtitle': 'Створіть акаунт Wheels Up і оберіть свою роль.',
        'button': 'Зареєструватися',
    })
    return render(request, template_name, {
        'form': form,
        'role_locked': bool(role),
        **role_content,
    })


def register_customer_view(request):
    return register_view(request, 'register/register.html', User.ROLE_CLIENT)


def register_driver_view(request):
    return register_view(request, 'register/register_driver.html', User.ROLE_DRIVER)


def register_admin_view(request):
    return register_view(request, 'register/register_admin.html', User.ROLE_MANAGER)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # ЗМІНЮЄМО ТУТ: замість 'home' відправляємо на розподілювач ролей
            return redirect('role_dashboard') 
    else:
        form = LoginForm()
    return render(request, 'login/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')
