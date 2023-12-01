from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def guest_reg(func):
    def register(request,**pk):
        if request.user.is_anonymous:
            token = request.COOKIES.get('csrftoken')
            if token:
                Guest.objects.get_or_create(token=token)
        return func(request,**pk)
    return register

@guest_reg
def home(request):
    slides = SliderImage.objects.all()
    products = Product.objects.all()
    category = request.GET.get('category')
    brands = request.GET.get('brand')
    product_pk = request.GET.get('pk')
    action = request.GET.get('action')
    search = request.GET.get('search')
    favorites = request.GET.get('favorites')
    guest = Guest.objects.filter(token = request.COOKIES.get('csrftoken')).last()
    

    if action == 'favorite':
        edit_cart(request,action,pk=product_pk)
        return redirect('store:home')
    if action == 'add_to_cart':
        add_to_cart(request, product_pk)
        return redirect('store:cart')
    elif action:
        if request.user.is_authenticated:
            edit_quan_user(user=request.user,action=action,pk=product_pk)
        else:
            user = guest
            edit_quan_user(user, action, product_pk)
        return redirect('store:home')
    
    products = Product.objects.filter(favorites=request.user) if favorites else products
    products = Product.objects.filter(Q(name__icontains=search) | Q(description__icontains=search)) if search else products
    products = products.filter(brand=brands) if brands else products
    products = products.filter(category=category) if category else products

    amount = show_amount(request)

    return render(request,'home.html', {'products': products, 'slides': slides, 'amount':amount})

@guest_reg
def product(request, pk):
    guest = Guest.objects.filter(token=request.COOKIES.get('csrftoken')).last()
    product_data = Product.objects.get(pk=pk)
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(product=product_data, customer = request.user).exists() 
    elif guest: 
        cart_items = CartItem.objects.filter(product=product_data, guest_customer = guest).exists()
    else:
        cart_items = None

    action = request.GET.get('action')
    
    
    if action == 'favorite':
        edit_cart(request,action,pk=pk)
        return redirect('store:product', pk=product_data.pk)
    
    if action == 'add_to_cart':
        add_to_cart(request, product_data.pk)
        return redirect('store:cart')

    amount = show_amount(request)

    form = RateForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.customer = request.user
        instance.product = product_data
        instance.save()
        return redirect('store:product', pk=product_data.pk)

    return render(request, 'product.html', {'product': product_data, 'cart_items': cart_items, 'amount':amount, 'form': form})


def add_to_cart(request,pk):
    guest = Guest.objects.filter(token = request.COOKIES.get('csrftoken')).last() 
    
    cart_items = CartItem.objects.filter(product=pk,guest_customer=guest if request.user.is_anonymous else None, customer = request.user if request.user.is_authenticated else None)
    
    if not cart_items:
        CartItem.objects.create(product=Product.objects.get(pk=pk),guest_customer = guest if request.user.is_anonymous else None, quantity=1, customer = request.user if request.user.is_authenticated else None)
    else:
        cart_items[0].quantity += 1
        cart_items[0].save()

    return redirect('store:cart')

@guest_reg
def cart(request):
    guest = Guest.objects.filter(token=request.COOKIES['csrftoken'])

    confirm_delete = False
    product_pk = request.GET.get('pk')
    action = request.GET.get('action')
    delete = request.GET.get('delete')

    # Неправильно работает удаление в корзине, удаляет последний объект

    if delete:
        confirm_delete = True
    if request.GET.get('confirm'):
        CartItem.objects.get(pk = request.GET.get('pk')).delete()
        # return redirect('store:cart')

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(customer=request.user)
    else:
        cart_items = CartItem.objects.filter(guest_customer = guest[0]) if guest else []
   
    if action:
        edit_cart(request, action, cart_items, product_pk)
        return redirect('store:cart')

    chosen_items = cart_items.filter(chosen=True) if cart_items else []

    total_sum = sum([i.total_price() for i in chosen_items])
    total_quan = sum([i.quantity for i in chosen_items])

    return render(request, 'cart.html', {'cart_items':cart_items,'total_sum':total_sum, 'confirm_delete': confirm_delete, 'total_quan': total_quan, 'chosen_items':chosen_items})


def edit_cart(request, action, cart_items=None, pk=None):
    cart_item = CartItem.objects.filter(pk=pk).last()
    if action:
        if action == 'delete_all':
            cart_items.delete()
        if action == 'choose':
            for i in cart_items:
                i.chosen = True
                i.save()
        if action == 'unchoose':
            for i in cart_items:
                i.chosen = False
                i.save()
        if action == 'delete_choosen':
            cart_items = CartItem.objects.filter(chosen=True)
            cart_items.delete()
        if action == 'chosen':
            cart_item.chosen = True
            cart_item.save()
        if action == 'unchosen':
            cart_item.chosen = False
            cart_item.save()
        if action == 'increment':
            cart_item.quantity += 1
            cart_item.save()
        if action == 'decrement' and cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        if action == 'favorite':
            product = Product.objects.get(pk=pk) 
            if request.user in product.favorites.all():
                product.favorites.remove(request.user)
            else:
                product.favorites.add(request.user)
            

def edit_quan_user(user,action,pk):
    cart_item = CartItem.objects.get(product=Product.objects.get(pk=pk),customer = user)
    if action == 'less_quan' and cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    elif action == 'less_quan' and cart_item.quantity == 1:
        cart_item.delete()
    else:
        cart_item.quantity += 1
        cart_item.save()

@login_required(login_url='/users/log_in/')
def create_order(request):
    cart_items = CartItem.objects.filter(customer=request.user, chosen = True) or None
    if not cart_items:
        return render(request, 'error.html', {})
    total_price = sum([i.total_price() for i in cart_items])
    amount = sum([i.quantity for i in cart_items])

    form = OrderForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(address = request.POST.get('address'), phone = request.POST.get('phone'), comments = request.POST.get('comments'), total_price = total_price, customer = request.user)
        for item in cart_items:
            OrderedProduct.objects.create(order = order, item = item.product, comments = request.POST.get('comments'), amount = item.quantity, total_price = item.total_price())
        cart_items.delete()
        return redirect('store:home')



    return render(request, 'order_create.html', {'cart_items': cart_items, 'total_price':total_price, 'amount':amount, 'form': form})

def edit_profile(request):
    form = EditProfileForm(request.POST or None, instance = request.user )
    if form.is_valid():
        form.save()
        return redirect('store:home')
    return render(request, 'edit_profile.html', {'form':form})


def orders(request):
    confirm_delete = False
    delete = request.GET.get('delete')
    
    if delete:
        confirm_delete = True
    if request.GET.get('confirm'):
        Order.objects.get(pk = request.GET.get('pk')).delete()
        return redirect('store:orders')


    user_orders = Order.objects.filter(customer = request.user)

    return render(request, 'orders.html', {'user_orders': user_orders,'confirm_delete': confirm_delete, 'delete': delete})

def favorite(request):
    favorites = Product.objects.filter(favorites=request.user)
    action = request.GET.get('action')
    pk = request.GET.get('pk')

    if action:
        edit_cart(request,action,pk=pk)
        return redirect('store:favorite')
        
    return render(request, 'favorite.html', {'favorites': favorites})


def show_amount(request):
    token =  request.COOKIES.get('csrftoken')

    guest = Guest.objects.filter(token=token).last()
    
    
    cart_items = CartItem.objects.filter(
        customer = request.user if request.user.is_authenticated else None,
        guest_customer = guest if request.user.is_anonymous else None
    )

    return sum([i.quantity for i in cart_items])                                                    


def edit_order(request, pk):
    order = Order.objects.get(pk=pk)
    form = OrderForm(request.POST or None, instance = order)

    # Как сделать, чтобы у юзера не показывалось поле статус
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('store:orders')
    return render(request, 'edit_order.html', {'form': form})


