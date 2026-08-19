from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ProductModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products_images/', null=True, blank=True)
    category = models.CharField(max_length=100)
    discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    @property
    def discounted_price(self):
        if self.discount:
            return self.price - (self.price * self.discount / 100)
        return self.price
    
class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.IntegerField()

    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

