from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutPage, name="logout"),
    path('search_user', views.search_user, name="search_user"),
    path('add_user_to_group/<id>/', views.add_user_to_group, name="add_user_to_group"),

    path('change_password/', views.changePassword, name="change_password"),
    path('reset_password/<int:id>/', views.resetPassword, name='reset_password'),
    path('staff_biodata/<int:id>/', views.staff_biodata, name='staff_biodata'),
]