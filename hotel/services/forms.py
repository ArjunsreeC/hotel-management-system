from django import forms
from .models import *

class ServicesForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(ServicesForm, self).__init__(*args, **kwargs)
        self.fields['service_type'].queryset = ServiceType.objects.all()
        self.fields['service_type'].label_from_instance = lambda obj: obj.name
        self.fields['room_reference'].queryset = Room.objects.all()
        self.fields['room_reference'].label_from_instance = lambda obj: obj.room_number

class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = '__all__'

class ParkingSpaceForm(forms.ModelForm):
    class Meta:
        model = ParkingSpace
        fields = '__all__'

class ParkingForm(forms.ModelForm):
    class Meta:
        model = ParkingSpace
        fields = ['vehicle_number', 'contact_number']

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'