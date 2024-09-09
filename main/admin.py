from django.contrib import admin
from . models import *



admin.site.register(Category)
admin.site.register(Meal)
admin.site.register(Request)
admin.site.register(RequestDetails)
admin.site.register(Roster)