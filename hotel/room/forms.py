from django import forms
from .models import *
from datetime import datetime, timedelta
from django.core.validators import MinValueValidator, MaxValueValidator

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room_type'].queryset = RoomType.objects.all()
        self.fields['room_type'].label_from_instance = lambda obj: obj.name

class RoomImageForm(forms.ModelForm):
    class Meta:
        model = RoomImage
        fields = ['image']

class RoomRateForm(forms.ModelForm):
    class Meta:
        model = RoomRate
        fields = ['date', 'amount', 'room_reference', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['room_reference'].queryset = Room.objects.all()
        self.fields['room_reference'].label_from_instance = lambda obj: obj.room_number
    
    def clean_is_active(self):
        cleaned_data = super().clean()
        is_active = cleaned_data.get('is_active')
        date = cleaned_data.get('date')
        room_reference = cleaned_data.get('room_reference')

        if is_active:
            existing_active_rates = RoomRate.objects.filter(
                room_reference=room_reference, is_active=True
            )

            if existing_active_rates.exists():
                raise forms.ValidationError(
                    f"Active RoomRate already exists for room {room_reference.room_number}.",
                )
            
            existing_active_rates = RoomRate.objects.filter(
                room_reference=room_reference, date=date
            )

            if existing_active_rates.exists():
                raise forms.ValidationError(
                    f"RoomRate already exists for room {room_reference.room_number} on {date}.",
                )
        return is_active
    
    def clean_date(self):
        cleaned_data = super().clean()
        date =  cleaned_data.get('date')
        if RoomRate.objects.filter(date=date).exists():
            raise forms.ValidationError(
                    f"RoomRate already exists for room on {date}.",
                )
        return date
    
class AmenitiesForm(forms.ModelForm):
    class Meta:
        model = Amenities
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room_reference'].queryset = Room.objects.all()
        self.fields['room_reference'].label_from_instance = lambda obj: obj.room_number
        self.fields['type'].queryset = AmenityType.objects.all()
        self.fields['type'].label_from_instance = lambda obj: obj.name

class AmenityTypeForm(forms.ModelForm):
    class Meta:
        model = AmenityType
        fields = '__all__'

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = '__all__'

class RoomSearchForm(forms.Form):
    default_start_date = datetime.now()
    default_end_date = datetime.now() + timedelta(days=5)

    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Start Date',
        initial=default_start_date
    )
    
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='End Date',
        initial=default_end_date
    )

    adults_count = forms.IntegerField(
        label='Adult',
        initial='2'
    )

from datetime import date, timedelta

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'is_food_included', 'adults_count', 'kids_count', 'additional_bed']
    selected_rooms = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)

        super().__init__(*args, **kwargs)

        # Set default check_in_date to today
        today = date.today()
        self.fields['check_in_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['check_in_date'].widget.attrs['value'] = today.strftime('%Y-%m-%d')

        # Set default check_out_date to 5 days after today
        default_check_out_date = today + timedelta(days=5)
        self.fields['check_out_date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['check_out_date'].widget.attrs['value'] = default_check_out_date.strftime('%Y-%m-%d')

    def clean_adults_count(self):
        selected_rooms = self.data.get('selected_rooms')
        adults_count = self.cleaned_data.get('adults_count')
        print("....selected_rooms......", selected_rooms)
        if selected_rooms:
            selected_rooms_list = [int(room_number) for room_number in selected_rooms.split(',')]
            total_capacity = self.room.max_capacity if self.room.room_number not in selected_rooms_list else 0
            print(total_capacity,"///////////")
            print(".....selected_rooms_list........", selected_rooms_list)
            capacity = sum(Room.objects.filter(room_number__in=selected_rooms_list).values_list('max_capacity', flat=True))
            total_capacity = capacity + total_capacity
            print(total_capacity)
            if adults_count > total_capacity:
                raise forms.ValidationError(
                    f"Max Guest is 5 per room. Do you want to upgrade/book multiple rooms."
                )
        return adults_count


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_type']

    amount = forms.DecimalField(
        label='Payment Amount',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = [
            'comments',
            'cleanliness_rating',
            'service_rating',
            'food_quality',
            'value_for_money',
            'overall_rating',
        ]

    cleanliness_rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    service_rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    food_quality = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    value_for_money = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    overall_rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )