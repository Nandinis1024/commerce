from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
   
    def __str__(self):
        return f"{self.id}: {self.username} {self.email} {self.password}"



class Category(models.Model):
    category_name = models.CharField(max_length=128, unique=True)


    def __str__(self):
        return self.category_name


class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)    
    bid_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")
      


class Listing(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="price")
    image = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="categories")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="listings")
    date_created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.title} {self.description} {self.price} {self.image}"


class Watchlist(models.Model):
    user_id =  models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")


class Comments(models.Model):
    comment_id =  models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_id")
    item_id = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_id")
    comment = models.CharField(max_length=1000, null=True)



