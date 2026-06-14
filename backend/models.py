
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# hare krishna

class Category(models.Model):
    category_name=models.CharField(max_length=50)
    slug=models.SlugField(max_length=30,unique=True)
    image=models.ImageField(upload_to='products/%Y/%m/%d')
    description=models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


    def __str__(self):
        return self.category_name
    

class Product(models.Model):
    product_name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=50,unique=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    description=models.TextField(blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    old_price=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    stock=models.PositiveBigIntegerField(default=1)
    available=models.BooleanField(default=True)
    weight=models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True,help_text="Weight in kg")
    main_image=models.ImageField(upload_to='products/%Y/%m/%d')
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    product_details=models.TextField(null=True,blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
    
    

    def __str__(self):
        return self.product_name
    

class Product_image(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image=models.ImageField(upload_to='gallery/%Y/%m/%d')

    def __str__(self):
        return self.product.product_name
    

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=20,blank=True,null=True)
    address=models.TextField(blank=True, null=True)
    location=models.TextField(blank=True,null=True)
    profile_image=models.ImageField(upload_to=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.product.product_name}"
    

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True)
    order_id=models.CharField(max_length=20,blank=True,null=True)
    full_name=models.CharField(max_length=20)
    phone=models.CharField(max_length=20,blank=True)
    address=models.TextField()
    location=models.CharField(max_length=50,blank=True,null=True)
    order_total=models.IntegerField(blank=True,null=True)
    order_status=models.CharField(max_length=20,
                                  choices=(('Pending','Pending'),
                                   ('Processing','Processing'),
                                   ('Completed','Completed'),
                                   ('Cancelled','Cancelled'),
                                  ),default='Pending')
    payment_type=models.CharField(max_length=50,null=True,blank=True)
    payment_status=models.CharField(max_length=20,default="Pending")
    transection_id=models.CharField(max_length=200,null=True,blank=True)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=20,decimal_places=2)

    def __str__(self):
        return f"{self.quantity} X {self.product.product_name}"
    
class Review(models.Model):
    product_name=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveSmallIntegerField()
    comment=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.product_name.product_name}-{self.rating}"
    
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_status = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=200, blank=True, null=True)
    payment_method = models.CharField(max_length=100, default="SSLCommerz")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"



