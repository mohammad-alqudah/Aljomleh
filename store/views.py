from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
from .utils import *

import json
import datetime

from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout 
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def p404(request):

    send_mail(
        'Subject here',
        'Here is the message.',
        'ef18110016@gmail.com',
        ['mohammad.y.qudah@gmail.com'],
        fail_silently=False,
    )
    context = {}
    return render(request, 'store/404-page.html', context)

def contact(request):
    context = {}
    return render(request, 'store/contact.html', context)



def index(request,category=None):
    print(category)
    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
        print (search)

    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    if category:
        
        category = Category.objects.get(name=category)
        print(category)
        products = Product.objects.filter(name__icontains = search,category=category)
    else:
        products = Product.objects.filter(name__icontains = search)

    
    products = checkIfItemInCart(request , items ,products)

    custom_range , products = paginator(request,products)
    try:
        customer = request.user.customer
    except:
        customer = ''
    categories = Category.objects.all()
    context = {'products':products, 'search':search,'custom_range':custom_range, 'customer':customer, "categories":categories, 'cartItems':cartItems, 'order':order}
    return render(request, 'store/index.html', context)




def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    if request.user.is_authenticated:
        customer = request.user.customer
    else:
        customer = ''
    context = {'items':items, 'order':order, 'cartItems':cartItems,"customer":customer}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    #    flavor = Flavor.objects.get(id=flavorId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product )#,flavor=flavor)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
    
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
            order.delevery_fee= 5
        order.save()
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['state'],
	)
        print(data['shipping']['address'])


    else:
        print('User is not logged in')

    return JsonResponse('Payment submitted..', safe=False)

def order_success(request,phone):
    customer = Customer.objects.get(phone=phone)
    order = Order.objects.filter(customer=customer).last()


    context = {"order":order}
    return render(request, 'store/order-success.html', context)

@login_required(login_url ='singin') 
def wishlist(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        wishlist =customer.wish_list.all()

    
        for product in wishlist:
            for item in items:
                if product.id == item.product.id:
                    product.quantity =  item.quantity
    else:
        customer = ''
        wishlist = ''
        



    
    context = {"wishlist":wishlist,'customer':customer}
    return render(request, 'store/wishlist.html', context)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    ShippingAddress.objects.create(
    customer=customer,
    order=order,
    address=data['shipping']['address'],
    neighborhood=data['shipping']['state'],

    )

    return JsonResponse('Payment submitted..', safe=False)

def login(request):
    if request.method == 'POST':
        phone  = request.POST["phone"]
        password = request.POST['password'] 
        try:
            customer  = Customer.objects.get(phone=phone) 
            username = customer.user.username
        except:
            print (" Customer does not exist ") 

        try:

            username = User.objects.get(username=username)
        except:
            print (" phone does not exist ") 
        print(username , password)
        print ("ok")
        user = authenticate(request, username = username, password=password) 

        if user is not None:
            auth_login(request,user)
            return redirect('index')
        else:
            print("username or password is incorect ")
        

    return render(request,"store/index.html" )

def signup(request):
    if request.method == 'POST':
        first_name  = request.POST["first_name"]
        last_name  = request.POST["last_name"]
        phone  = request.POST["phone"]
        password = request.POST['password'] 
        print (first_name,last_name,phone , password)
        try:
            user = User.objects.create_user(username= phone, password=password)
            

        except:
            print ("This account is already registered")

        user = User.objects.get(username=phone)
        customer =Customer(user= user, first_name=first_name, last_name=last_name, phone=phone )
        customer.save()

    

    return render(request,"store/index.html" )

def logoutUser(request):
    logout(request)
    return redirect('index')

def loginPage(request):

    return render(request, 'store/signin.html')

def signupPage(request):



    return render(request, 'store/signup.html')

def brand(request,brand):
    brand = Brand.objects.get(name=brand)
    products = Product.objects.filter(brand=brand)

    context = {"products":products,"brand":brand }
    return render(request, 'store/brand.html', context)

def receive_note(request):
    if request.method == 'POST':
        name  = request.POST["name"]
        phone = request.POST["phone"]
        message  = request.POST["message"]
        if request.user.is_authenticated:
            customer = request.user.customer
            data = ContactUs(customer=customer, name=name,phone=phone,message=message )
        else:
            data = ContactUs(name=name,phone=phone,message=message )
        data.save()
    return render(request,"store/index.html" )
 
def updateWishList(request):
    data = json.loads(request.body)
    productId = data['productId']
    product =Product.objects.get(id=productId)
    customer = request.user.customer


    if product in customer.wish_list.all():
        customer.wish_list.remove(product)
        customer.save()
        print ("remove")

    else:
        customer.wish_list.add(product)
        customer.save()
        print ("add")
    print('Product:', productId)
    return JsonResponse('Item was added', safe=False)

def filter_(request):
    categories = Category.objects.all()
    brands = Brand.objects.all()


    search = ''
    if request.GET.get('search'):
        search = request.GET.get('search')
        print (search)

    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.filter(name__icontains = search)

    
    products = checkIfItemInCart(request , items ,products)

    custom_range , products = paginator(request,products)
    try:
        customer = request.user.customer
    except:
        customer = ''
        print ("redirect + message")
    context = {'products':products, 'search':search,'custom_range':custom_range, 'customer':customer,'categories':categories,"brands":brands}

    return render(request, 'store/filter.html', context)