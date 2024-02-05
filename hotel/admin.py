from django.contrib import admin
from .user.models import *
from .room.models import *
from .services.models import *

admin.site.register(User)
admin.site.register(Room)
admin.site.register(RoomImage)
admin.site.register(RoomRate)
admin.site.register(RoomType)
admin.site.register(Amenities)
admin.site.register(AmenityType)
admin.site.register(Customer)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(ServiceType)
admin.site.register(Service)
admin.site.register(Menu)
admin.site.register(ParkingSpace)
admin.site.register(Rating)
