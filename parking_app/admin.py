from django.contrib import admin
from .models.parking_spot import ParkingSpot
from .models.vehicle import Vehicle
from .models.ticket import Ticket
from .models.abonne import Abonne
from .models.subscription import Subscription

admin.site.register(ParkingSpot)
admin.site.register(Vehicle)
admin.site.register(Ticket)
admin.site.register(Abonne)
admin.site.register(Subscription)
