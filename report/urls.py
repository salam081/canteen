from django.urls import path
from .import views

   
urlpatterns = [
    path('meal_report', views.meal_report_and_search, name='report'),
    path('report/pdf/', views.generate_pdf, name='meal_report_pdf'),
    path('user_report_details', views.user_report_details, name='user_report_details'),
]
   
