from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

STATE_CHOICES = [
        ('DHAKA', 'Dhaka'),
        ('CHITTAGONG', 'Chittagong'),
        ('RAJSHAHI', 'Rajshahi'),
        ('KHULNA', 'Khulna'),
        ('BARISAL', 'Barisal'),
        ('SYLHET', 'Sylhet'),
        ('RANGPUR', 'Rangpur'),
        ('MYMENSINGH', 'Mymensingh'),
    ]

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    locality = models.CharField(max_length=155)
    city = models.CharField(max_length=55)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=55)

    def __str__(self):
        return str(self.id)
    
CATEGORY_CHOICES=(
    ('M', 'Mobile'),
    ('L', 'Laptop'),
    ('TW', 'Top Wear'),
    ('BW', 'Bottom Wear'),
)

class Product(models.Model):
    title = models.CharField(max_length=155)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand  = models.CharField(max_length=155)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=5)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
STATUS_CHOICES =(
    ('Pending','Pending'),
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The way','On The way'),
    ('Delivered','Delivered'),
    ('Cancelled','Cancelled'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=55,choices=STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
