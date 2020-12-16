from django.shortcuts import render , redirect
from .models import *
from seller.models import *
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth import authenticate, login , logout 
from .filters import OrderFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.http import QueryDict
import copy
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def dashboard(request):
    if request.method == 'POST':
        return store(request)
    products = Product.objects.all()
    dash_products = products[:8]
    latest_prod = products.order_by('id')
    latest_prod = latest_prod[::-1]

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity
    else:
        items = []
        order = {'get_cart_total' : 0 , 'get_cart_quantity'  : 0 ,'shipping' : False}
        cartItems = order['get_cart_quantity']

    context = {
     'products' : products ,
     'product1' : products[0],
     'dash_products' : dash_products, 
     'cartItems' : cartItems ,
     'latest_prod' : latest_prod}
    return render(request, 'store/dashboard.html', context)

def store(request):


    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity
    else:
        items = []
        order = {'get_cart_total' : 0 , 'get_cart_quantity'  : 0 ,'shipping' : False}
        cartItems = order['get_cart_quantity']
    Allproducts = Product.objects.all()
    if request.method == 'POST':
        query = request.POST
        note = query.get('tag')   
        if note is None: 
            Allproducts = Allproducts.distinct
            context = {'products' : Allproducts , 'cartItems' : cartItems}
            return render(request,'store/store.html', context)
        note = note.split()
        for word in note:
            print(word)
            print(len(Allproducts))
            lookups = Q(tag__title__icontains = word)
            Allproducts = Allproducts.filter(lookups)
            print(len(Allproducts))


    Allproducts = Allproducts.distinct
    context = {'products' : Allproducts , 'cartItems' : cartItems}
    return render(request,'store/store.html', context)

def login_user(request):
    if request.user.is_authenticated:
        return dashboard(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request ,username=username, password=password)
        if user is not None:
            request.method = 'GET'
            login(request, user)
            return  dashboard(request)
    return render(request , 'store/login.html')

def logout_user(request):
    logout(request)
    return dashboard(request)

    return render(request,'store/login.html')
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity
    else:
        items = []
        order = {'get_cart_total' : 0 , 'get_cart_quantity'  : 0}
        cartItems = order['get_cart_quantity']
    context = {'items' : items ,'order' : order , 'cartItems' : cartItems ,'shipping' : False}
    return render(request,'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_quantity
    else:
        items = []
        order = {'get_cart_total' : 0 , 'get_cart_quantity'  : 0}
        cartItems = order['get_cart_quantity']
    context = {'items' : items ,'order' : order, 'cartItems' : cartItems ,'shipping' : False}
    return render(request,'store/checkout.html', context)

@csrf_exempt
def updateItem(request):
    productid = request.POST.get('id')
    action = request.POST.get('action')
    customer = request.user.customer
    product = Product.objects.get(id=productid)
    order,created = Order.objects.get_or_create(customer=customer)
    orderItem,created = OrderItem.objects.get_or_create(order=order , product=product) 
    if action == 'add':
        orderItem.quantity += 1
        sp = Seller_Product.objects.all().filter(product=product)
        cart_n = sp[0].cart_no
        sp.update(cart_no = cart_n+1)
    elif action == 'remove':
        orderItem.quantity -= 1
        sp = Seller_Product.objects.all().filter(product=product)
        cart_n = sp[0].cart_no
        sp.update(cart_no = cart_n-1)

    sp[0].save()
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    context = {'cart_quantity' : order.get_cart_quantity , 'cart_total' : order.get_cart_total , 'item_quantity' : orderItem.quantity , 'item_total' : orderItem.get_total}
    return JsonResponse(context, safe=False)

def ProcessOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()
        for item in order.orderitem_set.all():
            product = Seller_Product.objects.all().filter(product= item.product)
            initial_sale = product[0].sale
            product.update(sale = initial_sale+item.quantity)


        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
    else:
        print('user is not logged in..')
    return JsonResponse('payment complete', safe=False)

def product_detail(request ,id):

    product = Product.objects.get(id=id)
    context = {'product' : product}
    sp = Seller_Product.objects.all().filter(product=product)
    visit = sp[0].visits
    sp.update(visits = visit+1)
    #sp.save()
    return render(request, 'store/product.html', context)