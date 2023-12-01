from django.shortcuts import render, redirect
from store.models import *
from store.forms import *

def admin(request):
    orders = Order.objects.all()
    return render(request, 'admin.html', {'orders': orders})

def order(request, pk):
    order_data = Order.objects.get(pk=pk)
    return render(request, 'order.html', {'order': order_data})

def edit_order(request, pk):
    order = Order.objects.get(pk=pk)
    form = OrderForm(request.POST or None, instance = order)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('staff:order', pk=order.pk)
    return render(request, 'edit_order_admin.html', {'form': form})