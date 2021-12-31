import json
from .models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def cookieCart(request):

	#Create empty cart for now for non-logged in user
	try:
		cart = json.loads(request.COOKIES['cart'])
	except:
		cart = {}
		print('CART:', cart)

	items = []
	order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
	cartItems = order['get_cart_items']

	for i in cart:
		
		#We use try block to prevent items in cart that may have been removed from causing error
		try:
			cartItems += cart[i]['quantity']

			product = Product.objects.get(id=i)
			total = (product.price * cart[i]['quantity'])

			order['get_cart_total'] += total
			order['get_cart_items'] += cart[i]['quantity']

			item = {
				'id':product.id,
				'product':{'id':product.id,'name':product.name, 'price':product.price, 
				'imageURL':product.imageURL}, 'quantity':cart[i]['quantity'],
				'get_total':total,
				}
			items.append(item)

		except:
			pass
			
	return {'cartItems':cartItems ,'order':order, 'items':items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        #Create empty cart for now for non-logged in user
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems':cartItems ,'order':order, 'items':items}

def checkIfItemInCart (request , items, products):
    if request.user.is_authenticated:
        for item in items:
            for product in products:
                if product.id == item.product.id:
                    product.quantity =  item.quantity
                    break
    else:
        for item in items:
            for product in products:
                if product.id == item['product']['id']:
                    product.quantity =  item['quantity']
                    break

    return products

def guestOrder(request, data):

	first_name = data['form']['first_name']
	last_name = data['form']['last_name']

	phone = data['form']['phone']

	cookieData = cookieCart(request)
	items = cookieData['items']

	customer, created = Customer.objects.get_or_create(
			phone=phone,
			)
	customer.first_name = first_name
	customer.last_name = last_name

	customer.save()

	order = Order.objects.create(
		customer=customer,
		complete=False,
		)

	for item in items:
		product = Product.objects.get(id=item['id'])
		orderItem = OrderItem.objects.create(
			product=product,
			order=order,
			quantity=item['quantity'],
		)
	return customer, order

def paginator(request,objects):

    page = request.GET.get('page')
    results = 2
    paginator = Paginator(objects, results)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        objects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        objects = paginator.page(page)
    
    leftIndex = ( int(page) - 4 )
    if leftIndex < 1:
        leftIndex = 1 

    rightIndex = ( int(page) + 5 )
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages+ 1

    custom_range = range(leftIndex, rightIndex )
    return custom_range , objects


