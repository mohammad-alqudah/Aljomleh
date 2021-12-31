from django.db import models
from django.contrib.auth.models import User



class Category (models.Model):
    name = models.CharField(max_length=25)
    icon = models.CharField(max_length=10000, null=True ,  blank=True)
   
    def __str__(self):
        return self.name

class Brand (models.Model):
    name = models.CharField(max_length=25)
    description =  models.CharField(max_length=1000, null=True ,  blank=True)
    image=models.ImageField(null=True, blank=True)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '/images/imageNotFound.jpg'
        return url

   
    def __str__(self):
        return self.name

class Flavor (models.Model):
    name = models.CharField(max_length=25)
    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=40)
    price =models.DecimalField(max_digits=7, decimal_places=2)
    old_price=models.DecimalField(max_digits=7, decimal_places=2, null=True ,  blank=True )
    selling_price =models.DecimalField(max_digits=7, decimal_places=2)
    size = models.CharField(max_length=10)
    category =models.ForeignKey(Category, null=True ,  blank=True  , on_delete=models.SET_NULL)
    brand =models.ForeignKey(Brand, null=True ,  blank=True , on_delete=models.SET_NULL)
    image=models.ImageField(null=True, blank=True)
    flavor =models.ManyToManyField(Flavor, null=True  )
    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'images/imageNotFound.jpg'
        return url





class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=25, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_join = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=50)
    wish_list = models.ManyToManyField(Product,null=True, blank=True)
    phone = models.CharField(max_length=15, null=True)


    def __str__(self):
        return self.first_name +" "+ self.last_name
    
    @property
    def get_wishlist_count(self):
        wish_list = self.wish_list.all()
        total = 0
        for product in wish_list:
            total +=1
        return total



class PromoCode(models.Model):
	code = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	valid = models.CharField(max_length=15, null=True)
	count = models.IntegerField(default=0, null=True, blank=True)
	discount = models.CharField(max_length=50, null=True, blank=True)


	def __str__(self):
		return self.customer

class Order(models.Model):
	
    status_choices = (
        ('1', 'Placed Order'),
        ('2', 'Process Warehouse'),
		('3', 'With the driver'),
        ('4', 'delivered'),)
    status = models.CharField(max_length=1, choices=status_choices)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    promo_code =models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)
    delevery_fee = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total 

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total 

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    flavor =models.ManyToManyField(Flavor, null=True  )

    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.order)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=100, null=False)
	neighborhood = models.CharField(max_length=20, null=False)
	street = models.CharField(max_length=50, null=False)
	Name = models.CharField(max_length=50, null=False)
	Description = models.CharField(max_length=200, null=False)
	Long = models.CharField(max_length=200, null=False)
	Lat = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address


class ContactUs(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	name =  models.CharField(max_length=60, null=False)
	phone = models.CharField(max_length=60, null=False)
	message = models.CharField(max_length=2000, null=False)
	dateTime = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name

class NotifyMe(models.Model):
	email = models.EmailField(max_length = 60)


	def __str__(self):
		return self.name
