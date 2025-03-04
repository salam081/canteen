from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Department(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Department"

    def __str__(self):
        return self.title


class Unit(models.Model):
    title = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)


    class Meta:
        verbose_name_plural = "Unit"

    def __str__(self):
        return self.title
    
class Gender(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "gender"

    def __str__(self):
        return self.title

class UserGroup(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Role(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "role"

    def __str__(self):
        return self.title   

class User(AbstractUser):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    othername = models.CharField(max_length=100 ,blank=True,null=True)
    username = models.CharField(max_length=100, unique=True) 
    file_no = models.CharField(unique=True, max_length=7)
    phone_number = models.CharField(max_length=11,null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE,null=True)
    group = models.ForeignKey(UserGroup, on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['firstname', 'lastname', 'file_no', 'phone_number', 'department', 'unit']

    class Meta:
        verbose_name_plural = "User"

    # def __str__(self):
    #     return self.username

    def __str__(self):
        return f'{self.username} {self.firstname} {self.lastname} ({self.file_no}) {self.group}'