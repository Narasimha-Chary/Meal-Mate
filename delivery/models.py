from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    mobile = models.CharField(max_length=10)
    address = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.username}  {self.password}  {self.email}  {self.mobile}  {self.address}"
    
class Restaurant(models.Model):
    name = models.CharField(max_length=20)
    picture = models.URLField(max_length=200, default="https://www.flaticon.com/free-icon/placeholder_1147856")
    cuisine = models.CharField(max_length=200)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.name}  {self.cuisine}  {self.rating}/5 "
    
class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_items")
    name = models.CharField(max_length=20)
    picture = models.URLField(max_length=200, default="https://www.svgrepo.com/show/51691/placeholder.svg")
    description = models.CharField(max_length=200)
    price = models.FloatField()
    is_veg = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}  {self.description}  {self.price}"