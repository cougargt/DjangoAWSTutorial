# ---------------------------------------------------------
#  Assignment 3, Django Tutorial
#  Author: Daniel Zajac
#  Class:  ECE528
#  March 14, 2021
# ---------------------------------------------------------
from django.db import models

# Database model for a Vehicle Model
class VehModel(models.Model):
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)

    def __str__(self):
        return self.brand + ', ' + self.model

# Database model for a Specific Vehicle
class Vehicle(models.Model):
    VehModel = models.ForeignKey(VehModel, on_delete=models.CASCADE)
    title_status_salvage = models.BooleanField(default=False)
    year = models.IntegerField(default=1900)
    color = models.CharField(max_length=200)
    vin = models.CharField(max_length=200)

    def __str__(self):
        return self.VehModel.__str__() + ' Vin:' + self.vin

# Database model for a Specific Sale transaction
class Sale(models.Model):
    Vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    mileage = models.IntegerField(default=0)
    lot = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.Vehicle.__str__() + ' Lot:' + self.lot


