from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import logout, login
from store.models import *



def connect_data(request):
    guest = Guest.objects.filter(token = request.COOKIES['csrftoken']) 
    guest_cart_items = CartItem.objects.filter(guest_customer=guest[0]) if guest else []
    for item in guest_cart_items:
        if CartItem.objects.filter(customer = request.user,product = item.product).exists():
            user_cart_item = CartItem.objects.get(customer = request.user, product = item.product)
            user_cart_item.quantity += item.quantity
            user_cart_item.save()
            item.delete()
            guest.delete()
        else:
            item.customer = request.user
            item.guest_customer = None
            item.save()


def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('users:log_in')
    return render(request, 'registration.html', {'form':form})

def log_in(request):
    form = LoginForm(data=request.POST or None)
    
    if form.is_valid():
            user = form.get_user()
            login(request,user)
            connect_data(request)

            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            
            if user.is_staff and not user.is_superuser:
                return redirect('staff:home')
            # Если юзер является персоналом, по не является суперюзером
            
            return redirect('store:home')
    return render(request, 'log_in.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect('store:home')



