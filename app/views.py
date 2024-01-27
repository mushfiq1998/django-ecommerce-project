from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Customer, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        return render(request, 'app/home.html', {'topwears': topwears, 
            'bottomwears': bottomwears, 'mobiles': mobiles})

class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) 
            & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', 
        {'product': product, 'item_already_in_cart': item_already_in_cart})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('product_id')
    print('product_id: ', product_id)
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/show-cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        carts = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        if carts:
            for cart in carts:
                temp_amount = cart.quantity * (cart.product.discounted_price)
                amount += temp_amount
            totalamount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts': carts, 
            'totalamount': totalamount, 'amount': amount})
        else:
            return render(request, 'app/emptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        cart.quantity += 1
        cart.save()
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        # totalamount = amount + shipping_amount
        data = {
            'quantity': cart.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        cart.quantity -= 1
        cart.save()
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount

        data = {
            'quantity': cart.quantity,
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        product_id = request.GET['product_id']
        cart = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        cart.delete()
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount

        data = {
            'amount': amount,
            'totalamount': amount + shipping_amount
        }
        return JsonResponse(data)

def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required
def address(request):
    # A loggedin user may have more profiles (addresses)
    addresses = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', 
    {'addresses': addresses, 'active': 'btn-primary'})

@login_required
def orders(request):
    user = request.user
    orders = OrderPlaced.objects.filter(user=user)
    return render(request, 'app/orders.html', {'orders': orders})

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Redmi' or data == 'Samsung':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
    elif data == 'above':
        mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})

def laptop(request, data=None):
    if data == None:
        laptops = Product.objects.filter(category='L')
    elif data == 'Apple' or data == 'Hp' or data == 'Dell':
        laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        laptops = Product.objects.filter(category='L').filter(discounted_price__lt=50000)
    elif data == 'above':
        laptops = Product.objects.filter(category='L').filter(discounted_price__gt=50000)
    return render(request, 'app/laptop.html', {'laptops': laptops})

def topwear(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Yellow' or data == 'Lotto':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=500)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=500)
    return render(request, 'app/topwear.html', {'topwears': topwears})

def bottomwear(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category='BW')
    elif data == 'Yellow' or data == 'Lotto':
        bottomwears = Product.objects.filter(category='BW').filter(brand=data)
    elif data == 'below':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__lt=800)
    elif data == 'above':
        bottomwears = Product.objects.filter(category='BW').filter(discounted_price__gt=800)
    return render(request, 'app/bottomwear.html', {'bottomwears': bottomwears})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', 
        {'form': form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations !! \
            Registered successfully')
            form.save()
            # After saving the form return empty form
            form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', 
        {'form': form})

@login_required
def checkout(request):
    user = request.user
    addresses = Customer.objects.filter(user = user)
    cart_items = Cart.objects.filter(user = user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
            temp_amount = (p.quantity * p.product.discounted_price)
            amount += temp_amount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'addresses': addresses, 
        'totalamount': totalamount, 'cart_items': cart_items})

@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    carts = Cart.objects.filter(user=user)
    for cart in carts:
        OrderPlaced(user=user, customer=customer, product=cart.product, 
        quantity=cart.quantity).save()
        cart.delete()
    return redirect("orders")

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form': form, 
            'active': 'btn-primary'})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            customer = Customer(user=user, name=name, locality=locality, 
            city=city, state=state, zipcode=zipcode)
            customer.save()
            # form = CustomerProfileForm()
            messages.success(request, 'Congratulations !! \
            Profile Updated successfully')
        return render(request, 'app/profile.html', {'form': form, 
            'active': 'btn-primary'})
