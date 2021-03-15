# ---------------------------------------------------------
#  Assignment 3, Django Tutorial
#  Author: Daniel Zajac
#  Class:  ECE528
#  March 14, 2021
# ---------------------------------------------------------
from django.http import HttpResponse
from django.shortcuts import render
from .models import VehModel, Vehicle, Sale
from django.http import JsonResponse

# Our first Endpoint
def hello(request):
    return HttpResponse('Success!')

# Adding our first vehicle
def createOne(request):

    #Create the Model (Since we are starting with an Empty DB)
    theModel = VehModel(brand="Ford",model="Ranger")
    theModel.save()

    #Creae a new Vehicle
    theVehicle = Vehicle(
        VehModel = theModel,
        title_status_salvage = False,
        year = 2013,
        color = "Blue",
        vin = "1FTCR11AXDUB12345")
    theVehicle.save()

    #Generate a new Sale entry
    theSale = Sale(
        Vehicle = theVehicle,
        mileage = 12345,
        lot = "9607-892",
        state = "Michigan",
        country = "USA",
        price = 1900)
    theSale.save()

    # get the total number of vehicles from the DB
    count = len(Vehicle.objects.all())

    # generate a response to the browser.
    return HttpResponse("Added: " + str(theVehicle) + " " + str(theSale) +"<br>Total Vehicles in DB: " +str(count))

# Creating a Piechart
def pie_chart(request):
    #create a dicitonary to prepare our response.
    colors = dict()

    #Manage the number of colors we will report
    all_colors = ['red', 'green', 'blue', 'black', 'silver', 'white', 'yellow', 'orange', 'gold']

    # Initalize our buckets
    for color in all_colors:
        colors[color]=0
    colors['other'] = 0

    # get ALL the vehicles from the DB
    queryset = Vehicle.objects.all()

    # go through each one, and match the colors
    for car in queryset:
        found = False
        for color in all_colors:
            if color in car.color.lower():
                colors[color] +=1
                found = True
                break

        # if we don't match any colors, put it in "others"
        if not found:
            colors['other'] +=1

    # create and render a response from the template
    return render(request, 'pie-chart.html', {
        'labels': list(colors.keys()),
        'data': list(colors.values()),
        'colors': list(all_colors)
    })

# This renders the Template Page
def sales_chart(request):
    return render(request, 'sales-chart.html')

# This renders Just JSON from the database prepared for Sales_Chart view
# this takes a long time, so using the other page to reference this one
# indirectly lets us add spinning wheels or show other content while the
# backend prepares the database.
def sales_data(request):

    # Create a dictionary for our response
    data = dict()

    # fetch ALL the sales
    queryset = Sale.objects.all()

    # Go through each Sale and sum up the sale price by Make
    for entry in queryset:
        if entry.Vehicle.VehModel.brand in data.keys():
            data[entry.Vehicle.VehModel.brand] += entry.price
        else:
            data[entry.Vehicle.VehModel.brand] = entry.price

    # Sort the data
    data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    # prepare a response as JSON
    return JsonResponse(data={
        'labels': list(data.keys()),
        'data': list(data.values()),
    })

# this view will pull in the CSV and populate the tables in the DB.
def csvReader(request):
    import csv

    # read the CSV File and create VehModels, Vehicles, and Sales entries
    with open('USA_cars_datasets.csv') as csvfile:
        vehicleReader = csv.reader(csvfile, delimiter=',')
        next(vehicleReader, None)
        for row in vehicleReader:
            print (row)

            # not in the DB already, Add veh Model
            if VehModel.objects.filter(brand = row[2]).filter(model = row[3]).count() == 0:
                newVehModel = VehModel(brand= row[2], model= row[3])
                newVehModel.save()
            else:
                newVehModel = VehModel.objects.filter(brand = row[2]).filter(model = row[3])[0]

            if Vehicle.objects.filter(vin=row[8].strip()).count() == 0:
                newVehicle = Vehicle(
                    VehModel=newVehModel,
                    title_status_salvage=(row[5]=='clean vehicle'),
                    year=row[4],
                    color=row[7],
                    vin=row[8].strip()
                )
                newVehicle.save()
            else:
                newVehicle = Vehicle.objects.filter(vin=row[8].strip())[0]

            if Sale.objects.filter(lot=row[9].strip()).count() == 0:
                newSale = Sale(
                    Vehicle =newVehicle,
                    mileage = int(float(row[6])),
                    lot = row[9],
                    state = row[10],
                    country = row[11],
                    price = row[1]
                )
                newSale.save()

    count = len(Sale.objects.all())
    return HttpResponse('Done. Loaded: ' + str(count) + 'Transactions')
