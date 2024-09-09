from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('admin_page', views.admin_page, name="admin_page"),
    path('canteen_manager', views.canteen_manager, name="canteen_manager"),
    path('delete_meal/<str:id>/', views.delete_meal, name="delete_meal"),
    path('meal_request', views.meal_request, name="meal_request"),
    path('add_staff_on_call', views.add_staff_on_call, name="add_staff_on_call"),
    path('user_roster', views.user_roster, name="user_roster"),
    path('meal_request_details', views.meal_request_details, name="meal_request_details"),    
    path('edit_meal_request/<str:id>/', views.edit_meal_request, name="edit_meal_request"), 
    path('delete_meal_request/<str:id>/', views.delete_meal_request, name="delete_meal_request"), 
    
]   