from django.contrib import admin
from .models.parking_spot import ParkingSpot
from .models.vehicle import Vehicle
from .models.ticket import Ticket

admin.site.register(ParkingSpot)
admin.site.register(Vehicle)
admin.site.register(Ticket)
