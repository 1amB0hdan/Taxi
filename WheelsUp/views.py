from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import UserProfile, Order, OrderNotification
from .forms import (
    UserRegistrationForm, CustomerRegistrationForm, 
    DriverRegistrationForm, AdminRegistrationForm, OrderForm
)

# Create your views here.
def home(request):
    service_cards = [
        {
            'title': 'Поїздки',
            'description': 'Швидкий виклик авто для повсякденних поїздок. Комфортні класи, чисті автомобілі та професійні водії.',
            'list_items': [
                'Подання від 3 хвилин',
                'По місту та передмістю',
                'Оплата готівкою та карткою',
            ]
        },
        {
            'title': 'Доставка',
            'description': 'Експрес-доставка документів, посилок та особистих речей по місту без зайвих затримок.',
            'list_items': [
                'Термінова доставка',
                'Безпечна передача',
                'Відстеження кур'єра',
            ]
        },
        {
            'title': 'Вантажне таксі',
            'description': 'Переїзд, доставка меблів та великогабаритних вантажів. Є спеціалізовані вантажні автомобілі.',
            'list_items': [
                'Місткі фургони',
                'Доставка до дверей',
                'Допомога з навантаженням',
            ]
        },
        {
            'title': 'Для бізнесу',
            'description': 'Корпоративні поїздки та доставка для компаній з прозорим обліком та підтримкою 24/7.',
            'list_items': [
                'Корпоративні тарифи',
                'Щомісячний звіт',
                'Індивідуальні маршрути',
            ]
        },
    ]
    context = {
        'service_cards': service_cards
    }
    return render(request, 'home/home.html', context)

def services(request):
    return render(request, 'services/services.html')

def about(request):
    return render(request, 'about/about.html')

def contacts(request):
    return render(request, 'contacts/contacts.html')


# ============= AUTHENTICATION VIEWS =============

def register_customer(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone')
            
            # Create user profile
            UserProfile.objects.create(
                user=user,
                user_type='customer',
                phone=phone
            )
            
            # Auto-login
            login(request, user)
            messages.success(request, 'Ви успішно зареєстровалися як заказчик!')
            return redirect('dashboard')
    else:
        form = CustomerRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Реєстрація Заказчика',
        'user_type': 'customer'
    }
    return render(request, 'register/register.html', context)


def register_driver(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = DriverRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = form.cleaned_data.get('phone')
            
            # Create user profile for driver
            UserProfile.objects.create(
                user=user,
                user_type='driver',
                phone=phone
            )
            
            # Auto-login
            login(request, user)
            messages.success(request, 'Ви успішно зареєстровалися як водій!')
            return redirect('driver_dashboard')
    else:
        form = DriverRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Реєстрація Водія',
        'user_type': 'driver'
    }
    return render(request, 'register/register_driver.html', context)


def register_admin(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    
    admin_code = 'ADMIN_SECRET_2024'  # Змініть на свій код
    
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            submitted_code = form.cleaned_data.get('admin_code')
            
            if submitted_code != admin_code:
                messages.error(request, 'Неправильний адмін-код!')
                return render(request, 'register/register_admin.html', {'form': form})
            
            user = form.save()
            phone = form.cleaned_data.get('phone')
            
            # Create user profile for admin
            UserProfile.objects.create(
                user=user,
                user_type='admin',
                phone=phone,
                is_verified=True
            )
            
            # Auto-login
            login(request, user)
            messages.success(request, 'Ви успішно зареєстровалися як адміністратор!')
            return redirect('admin_dashboard')
    else:
        form = AdminRegistrationForm()
    
    context = {
        'form': form,
        'title': 'Реєстрація Адміністратора',
        'user_type': 'admin'
    }
    return render(request, 'register/register_admin.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Вітаємо, {user.first_name}!')
                
                # Redirect based on user type
                try:
                    if user.profile.user_type == 'driver':
                        return redirect('driver_dashboard')
                    elif user.profile.user_type == 'admin':
                        return redirect('admin_dashboard')
                except:
                    pass
                
                return redirect('dashboard')
            else:
                messages.error(request, 'Неправильна email або пароль')
        except Exception as e:
            messages.error(request, f'Помилка при входу: {str(e)}')
    
    return render(request, 'login/login.html')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Ви вийшли з акаунту')
    return redirect('home')


# ============= DASHBOARD VIEWS =============

@login_required(login_url='login')
def profile_view(request):
    try:
        profile = request.user.profile
    except:
        messages.error(request, 'Профіль не знайдено')
        return redirect('home')
    
    context = {
        'profile': profile,
        'user': request.user
    }
    return render(request, 'profile/profile.html', context)


@login_required(login_url='login')
def dashboard(request):
    try:
        profile = request.user.profile
        if profile.user_type == 'customer':
            return customer_dashboard(request)
        elif profile.user_type == 'driver':
            return redirect('driver_dashboard')
        elif profile.user_type == 'admin':
            return redirect('admin_dashboard')
    except:
        pass
    
    return render(request, 'profile/profile.html')


def customer_dashboard(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    notifications = OrderNotification.objects.filter(recipient=request.user, is_read=False)
    
    context = {
        'orders': orders,
        'notifications': notifications,
        'unread_count': notifications.count()
    }
    return render(request, 'dashboard/customer_dashboard.html', context)


@login_required(login_url='login')
def driver_dashboard(request):
    try:
        profile = request.user.profile
        if profile.user_type != 'driver':
            messages.error(request, 'У вас немає доступу до цієї сторінки')
            return redirect('dashboard')
    except:
        messages.error(request, 'Профіль не знайдено')
        return redirect('home')
    
    # Get pending orders and assigned orders
    pending_orders = Order.objects.filter(status='pending')
    my_orders = Order.objects.filter(driver=request.user).exclude(status='completed')
    notifications = OrderNotification.objects.filter(recipient=request.user, is_read=False)
    
    context = {
        'pending_orders': pending_orders,
        'my_orders': my_orders,
        'notifications': notifications,
        'profile': profile,
        'unread_count': notifications.count()
    }
    return render(request, 'dashboard/driver_dashboard.html', context)


@login_required(login_url='login')
def admin_dashboard(request):
    try:
        profile = request.user.profile
        if profile.user_type != 'admin':
            messages.error(request, 'У вас немає доступу до цієї сторінки')
            return redirect('dashboard')
    except:
        messages.error(request, 'Профіль не знайдено')
        return redirect('home')
    
    all_orders = Order.objects.all().order_by('-created_at')
    pending_orders = Order.objects.filter(status='pending').count()
    completed_orders = Order.objects.filter(status='completed').count()
    drivers_count = UserProfile.objects.filter(user_type='driver').count()
    customers_count = UserProfile.objects.filter(user_type='customer').count()
    
    context = {
        'all_orders': all_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'drivers_count': drivers_count,
        'customers_count': customers_count,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


# ============= ORDER VIEWS =============

@login_required(login_url='login')
def create_order(request):
    try:
        profile = request.user.profile
        if profile.user_type != 'customer':
            messages.error(request, 'Тільки заказчики можуть створювати замовлення')
            return redirect('dashboard')
    except:
        messages.error(request, 'Профіль не знайдено')
        return redirect('home')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer = request.user
            order.save()
            
            # Create notifications for all drivers and admins
            drivers = UserProfile.objects.filter(user_type='driver').values_list('user', flat=True)
            admins = UserProfile.objects.filter(user_type='admin').values_list('user', flat=True)
            
            notification_message = (
                f"Нове замовлення! \n"
                f"Від: {request.user.first_name} {request.user.last_name}\n"
                f"Телефон: {request.user.profile.phone}\n"
                f"Звідки: {order.pickup_location}\n"
                f"Куди: {order.dropoff_location}\n"
                f"Тип послуги: {order.get_service_type_display()}\n"
                f"Орієнтовна вартість: {order.estimated_price or 'Не визначена'}"
            )
            
            for driver_id in drivers:
                OrderNotification.objects.create(
                    order=order,
                    recipient_id=driver_id,
                    message=notification_message
                )
            
            for admin_id in admins:
                OrderNotification.objects.create(
                    order=order,
                    recipient_id=admin_id,
                    message=notification_message
                )
            
            messages.success(request, 'Замовлення успішно створено! Водій незабаром прийме його.')
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()
    
    context = {'form': form}
    return render(request, 'orders/create_order.html', context)


@login_required(login_url='login')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Check permissions
    if order.customer != request.user and request.user.profile.user_type != 'admin':
        if request.user.profile.user_type == 'driver' and order.driver != request.user:
            messages.error(request, 'У вас немає доступу до цього замовлення')
            return redirect('dashboard')
    
    context = {'order': order}
    return render(request, 'orders/order_detail.html', context)


@login_required(login_url='login')
@require_http_methods(["POST"])
def accept_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    try:
        profile = request.user.profile
        if profile.user_type != 'driver':
            return JsonResponse({'success': False, 'error': 'Тільки водії можуть приймати замовлення'})
    except:
        return JsonResponse({'success': False, 'error': 'Профіль не знайдено'})
    
    if order.status != 'pending':
        return JsonResponse({'success': False, 'error': 'Це замовлення вже прийнято'})
    
    order.driver = request.user
    order.status = 'accepted'
    order.accepted_at = timezone.now()
    order.save()
    
    # Notify customer and admins
    customer_message = (
        f"Ваше замовлення прийнято!\n"
        f"Водій: {request.user.first_name} {request.user.last_name}\n"
        f"Телефон водія: {request.user.profile.phone}\n"
        f"Рейтинг: {request.user.profile.rating}★"
    )
    
    OrderNotification.objects.create(
        order=order,
        recipient=order.customer,
        message=customer_message
    )
    
    admins = UserProfile.objects.filter(user_type='admin').values_list('user', flat=True)
    admin_message = (
        f"Замовлення #{order.id} прийнято водієм {request.user.first_name} {request.user.last_name}"
    )
    for admin_id in admins:
        OrderNotification.objects.create(
            order=order,
            recipient_id=admin_id,
            message=admin_message
        )
    
    return JsonResponse({'success': True, 'message': 'Замовлення прийнято!'})


@login_required(login_url='login')
@require_http_methods(["POST"])
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if order.driver != request.user:
        return JsonResponse({'success': False, 'error': 'Це не ваше замовлення'})
    
    if order.status not in ['in_progress', 'accepted']:
        return JsonResponse({'success': False, 'error': 'Замовлення не можна завершити'})
    
    order.status = 'completed'
    order.completed_at = timezone.now()
    order.save()
    
    # Notify customer
    completion_message = (
        f"Ваше замовлення завершено!\n"
        f"Водій: {request.user.first_name} {request.user.last_name}\n"
        f"Подякуйте водієм та залиште відгук"
    )
    
    OrderNotification.objects.create(
        order=order,
        recipient=order.customer,
        message=completion_message
    )
    
    return JsonResponse({'success': True, 'message': 'Замовлення завершено!'})


@login_required(login_url='login')
def notifications(request):
    notifications = OrderNotification.objects.filter(recipient=request.user).order_by('-created_at')
    
    # Mark as read
    unread = notifications.filter(is_read=False)
    unread.update(is_read=True)
    
    context = {'notifications': notifications}
    return render(request, 'notifications/notifications.html', context)
