# ---------------------------------------------------------
#  Assignment 3, Django Tutorial
#  Author: Daniel Zajac
#  Class:  ECE528
#  March 14, 2021
# ---------------------------------------------------------
from django.urls import path

from . import views

urlpatterns = [
    path('', views.hello, name='hello'),
    path('createOne', views.createOne, name='createOne'),
    path('csvReader', views.csvReader, name='csvReader'),
    path('pie-chart', views.pie_chart, name='pie-chart'),
    path('sales-chart/', views.sales_chart, name='sales-chart'),
    path('sales-data/', views.sales_data, name='sales-data'),
]