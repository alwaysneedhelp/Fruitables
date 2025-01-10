from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Profile
from shopper.models import Address, CartOrder, CartOrderItems
import calendar
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .decorators import admin_required

@login_required
def profile(request):

    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    address = Address.objects.filter(user=request.user)

    orders_analyse = CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month', 'count')

    
    monthes = []
    total_orders = []

    for o in orders_analyse:
        monthes.append(calendar.month_name[o['month']])
        total_orders.append(o['count'])

    total_orders.append(100)

    try:
        user_profile = Profile.objects.get(user=request.user)
    except:
        user_profile = None

    context = {
        'orders': orders,
        'address':address,
        'monthes':monthes,
        'total_orders':total_orders,
        'user_profile':user_profile,
    }

    return render(request, 'profile_page/main_profile.html', context)

def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    products = CartOrderItems.objects.filter(order=order)

    context = {
        'products': products,
        'order': order,
    }

    return render(request, 'profile_page/order_detail.html', context)


def logout_func(request):
    logout(request)
    return redirect('home')

def make_address_default(request):
    pass

@login_required
def change_password(request):
    user = request.user

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm = request.POST.get('confirm')

        if confirm != new_password:
            messages.error(request, 'Password Does Not Match')
            return redirect('change_password')
        
        if check_password(old_password, user.password):
            username = user.username
            user.set_password(new_password)
            user.save()
            new_user = authenticate(request, username=username, password=new_password)
            login(request, new_user)
            messages.success(request, 'Password Changed Successfully')
            return redirect('change_password')
        else:
            messages.error(request, 'Old Password Is Incorrect')
            return redirect('change_password')
        
    return render(request, 'profile_page/change_password.html')