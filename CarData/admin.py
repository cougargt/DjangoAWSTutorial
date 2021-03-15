# ---------------------------------------------------------
#  Assignment 3, Django Tutorial
#  Author: Daniel Zajac
#  Class:  ECE528
#  March 14, 2021
# ---------------------------------------------------------
from django.contrib import admin
from .models import VehModel, Vehicle, Sale

# Create an Admin Interface for Vehicle Model
class AdminVehModel(admin.ModelAdmin):
    fields = ['brand', 'model']

# Create an Admin Interface for Vehicle
class AdminVehicle(admin.ModelAdmin):
    fields = [
        'VehModel',
        'title_status_salvage',
        'year',
        'color',
        'vin',
    ]

# Create an Admin Interface for Sale
class AdminSale(admin.ModelAdmin):
    fields = [
        'Vehicle',
        'mileage',
        'lot',
        'state',
        'country',
        'price'
    ]

# Register all three with the Admin Interface
admin.site.register(VehModel, AdminVehModel)
admin.site.register(Vehicle, AdminVehicle)
admin.site.register(Sale, AdminSale)
