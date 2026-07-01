from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order

@login_required(login_url='/accounts/login/')
def role_dashboard(request):
    user = request.user

    if user.is_staff or 'driver' in user.username.lower() or user.username.lower() == 'wodiy':
        orders = Order.objects.all().order_by('-id')
        return render(request, 'ordersa/orders.html', {'orders': orders})
    else:
        messages.warning(request, "Клієнти керують замовленнями з головної сторінки.")
        return redirect('home')


@login_required(login_url='/accounts/login/')
def create_order(request):
    if request.method == 'POST':
        pickup = request.POST.get('pickup_location')
        dropoff = request.POST.get('dropoff_location')
        order_time = request.POST.get('order_time', 'Зараз')
        
        if pickup and dropoff:
            Order.objects.create(
                client=request.user,
                pickup_location=pickup,
                dropoff_location=dropoff,
                status='Pending'
            )
            messages.success(request, f"Ваше замовлення на час '{order_time}' успішно прийнято!")
            return redirect('home')
            
    return redirect('home')


@login_required(login_url='/accounts/login/')
def driver_take_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Accepted'
    order.save()
    messages.success(request, f"Ви прийняли замовлення #{order_id}!")
    return redirect('role_dashboard')


@login_required(login_url='/accounts/login/')
def driver_complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'Completed'
    order.save()
    messages.success(request, f"Замовлення #{order_id} успішно виконано!")
    return redirect('role_dashboard')