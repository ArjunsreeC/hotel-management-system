from rest_framework import serializers
from .models import *
from django.db.models import Avg, Min, Max
from datetime import datetime, timedelta

class RoomSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        self.start_date = kwargs.pop('start_date', datetime.now())
        self.end_date = kwargs.pop('end_date', datetime.now() + timedelta(days=5))
        self.days = kwargs.pop('days', 5)
        super(RoomSerializer, self).__init__(*args, **kwargs)

    room_rates = serializers.SerializerMethodField()
    room_type = serializers.SerializerMethodField()
    room_rating = serializers.SerializerMethodField()


    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'max_capacity', 'room_description', 'room_rates', 'room_rating']

    def get_room_rates(self, obj):
        result=None
        try:
            active_room_rate = active_room_rate = RoomRate.objects.filter(
                room_reference=obj,
                date__range=(self.start_date, self.end_date)
            )
        except RoomRate.DoesNotExist:
            active_room_rate = None
        if active_room_rate.exists():
            average_amount = active_room_rate.aggregate(avg_amount=Avg('amount'))['avg_amount']
            lowest_amount = active_room_rate.aggregate(min_amount=Min('amount'))['min_amount']
            highest_amount = active_room_rate.aggregate(max_amount=Max('amount'))['max_amount']
            result = {
            'average': round(average_amount*self.days, 2),
            'lowest': lowest_amount*self.days,
            'highest': highest_amount*self.days,
        }
        else:
            result = {
            'average': 750*self.days,
            'lowest': 500*self.days,
            'highest': 1000*self.days,
        }
        return result
    
    def get_room_rating(self, obj):
        last_5_ratings = Rating.objects.filter(booking_reference__room=obj).order_by('-booking_reference__booking_date')[:5]
        average_rating = last_5_ratings.aggregate(avg_rating=Avg('overall_rating'))['avg_rating']
        return round(average_rating / 2) if average_rating else 0
    
    def get_room_type(self, obj):
        return obj.room_type.name
    
class RoomRateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomRate
        fields = '__all__'

class RoomTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomType
        fields = '__all__'

class AmenitiesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Amenities
        fields = '__all__'

class AmenityTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AmenityType
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'

    check_in_status = serializers.SerializerMethodField()
    canceled_rooms = serializers.SerializerMethodField()
    room = RoomSerializer(read_only=True, many=True)

    def get_check_in_status(self, obj):
        return obj.check_in_date <= datetime.now().date() <= obj.check_out_date   
    
    def get_canceled_rooms(self, obj):
        # Convert the comma-separated string to a list
        canceled_rooms = obj.canceled_rooms.split(',') if obj.canceled_rooms else []
        return canceled_rooms