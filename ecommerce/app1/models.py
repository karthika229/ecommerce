from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    categoryname = models.CharField(max_length=255)

    def __str__(self):
        return self.categoryname

class Product(models.Model):
    productname = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)    
    image=models.FileField(upload_to='image/',null=True)

    def __str__(self):
        return self.productname
    
class Customer(models.Model):
    
    address=models.CharField(max_length=255)
    phone=models.CharField(max_length=20)
    image=models.FileField(upload_to='image/',null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def _str_(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

    @property
    def total_price(self):
        return self.quantity * self.product.price 