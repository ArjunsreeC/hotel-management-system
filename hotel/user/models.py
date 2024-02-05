from django.db import models

ACCESS_TYPE_CHOICES = (
        ('Admin', 'Admin'),
        ('Owner', 'Owner'),
        ('Staff', 'Staff'),
        ('Customer', 'Customer'),
    )

DIETARY_PREFERENCE_CHOICES = [
        ('veg', 'Vegetarian'),
        ('non-veg', 'Non-Vegetarian'),
        ('custom', 'Custom')
    ]

CUSTOMER_TIER_CHOICES = [
        ('premium', 'Premium'),
        ('normal', 'Normal'),
    ]

class User(models.Model):
    email = models.EmailField()
    age = models.IntegerField()
    address = models.TextField()
    contact_number = models.CharField()
    access_type = models.CharField(
        max_length=20,
        choices=ACCESS_TYPE_CHOICES,
        default='Customer',
    )
    password = models.CharField(default="test")


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    user = models.OneToOneField('User', on_delete=models.CASCADE, default=1)
    tier = models.CharField(
        max_length=10,
        choices=CUSTOMER_TIER_CHOICES,
        default='premium'
    )
    dietary_preference = models.CharField(
        max_length=10,
        choices=DIETARY_PREFERENCE_CHOICES,
        default='custom'
    )