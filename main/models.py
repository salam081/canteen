from django.db import models
from datetime import date
from accounts.models import *

class Category(models.Model):
    title = models.CharField(blank=True, null=True, max_length=25)

    class Meta:
        verbose_name_plural = "Category"

    def __str__(self):
        return self.title

class Meal(models.Model):
    title = models.CharField(max_length=25)
    price = models.CharField(max_length=7)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    meals_image = models.ImageField(upload_to='meal_image', default='default.png', blank=True,null=True)
    class Meta:
        verbose_name_plural = "Meal"

    def __str__(self):
        return self.title

class Request(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Decline', 'Decline'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=8,choices=STATUS_CHOICES,default='Pending')
    
    class Meta:
        verbose_name_plural = "Request"

    def __str__(self):
        return str(self.user)

class RequestDetails(models.Model):
    request = models.ForeignKey(Request, on_delete=models.SET_NULL, null=True)
    meal = models.ForeignKey(Meal, on_delete=models.SET_NULL, null=True)
   

    class Meta:
        verbose_name_plural = "RequestDetail"

    def __str__(self):
        return str(f'{self.request} {self.meal}')

class Roster(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    
    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date}"






