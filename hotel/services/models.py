from django.db import models
from hotel.room.models import Room
from hotel.user.models import User

class ServiceType(models.Model):
    name = models.CharField(max_length=10)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=1000)

class Service(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    service_id = models.AutoField(primary_key=True)
    service_type = models.ForeignKey('ServiceType', on_delete=models.CASCADE, default=1)
    description = models.TextField()
    status = models.BooleanField(default=False)
    room_reference = models.ForeignKey(Room, on_delete=models.CASCADE, default=1)

class Menu(models.Model):

    ITEM_TYPES = [
        ('food', 'Food'),
        ('beverages', 'Beverages'),
    ]

    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=ITEM_TYPES)
    description = models.TextField()
    prize = models.DecimalField(max_digits=10, decimal_places=2)

class ParkingSpace(models.Model):
    parking_id = models.AutoField(primary_key=True)
    is_booked = models.BooleanField(default=False)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['parking_id']