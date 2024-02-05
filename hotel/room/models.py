from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from hotel.user.models import Customer, User

class RoomType(models.Model):
    name = models.CharField(max_length=10)

class Room(models.Model):
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey('RoomType', on_delete=models.CASCADE, default=1)
    max_capacity = models.PositiveIntegerField()
    room_description = models.TextField()

class RoomImage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images/')

class RoomRate(models.Model):
    date = models.DateField(default=timezone.now)
    is_available = models.BooleanField(default=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    room_reference = models.ForeignKey('Room', on_delete=models.CASCADE, default=101)
    is_active = models.BooleanField(default=False)

class AmenityType(models.Model):
    name = models.CharField(max_length=10)

class Amenities(models.Model):
    AMENITY_STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Damaged', 'Damaged'),
    )

    type = models.ForeignKey('AmenityType', on_delete=models.CASCADE, default=1)
    purchase_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=8, choices=AMENITY_STATUS_CHOICES, default='active')
    room_reference = models.ForeignKey('Room', on_delete=models.CASCADE, default='101')

BOOKING_STATUS_CHOICES = (
        ('Reservation', 'Reservation'),
        ('CheckedIn', 'CheckedIn'),
        ('Canceled', 'Canceled'),
        ('CheckedOut', 'CheckedOut'),
    )

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    room = models.ManyToManyField('Room')
    booking_date = models.DateField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_days = models.PositiveIntegerField()
    is_food_included = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES)
    adults_count = models.IntegerField(default=1)
    kids_count = models.PositiveSmallIntegerField(default=0)
    additional_bed = models.BooleanField(default=False)
    canceled_rooms = models.TextField(null=True, blank=True)


class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('declined', 'Declined'),
    )

    PAYMENT_TYPE_CHOICES = (
        ('cash', 'Cash'),
        ('check', 'Check'),
        ('upi', 'UPI'),
        ('card', 'Card'),
    )

    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateField()
    booking_reference = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPE_CHOICES)

class Rating(models.Model):
    booking_reference = models.OneToOneField(Booking, on_delete=models.CASCADE)
    comments = models.TextField(blank=True, null=True)
    cleanliness_rating = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    service_rating = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    food_quality = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    value_for_money = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    overall_rating = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )