from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import *
from hotel.user.models import User
from .serializers import *
from .forms import *
from django.http import HttpResponseForbidden

class ServicesListView(View):
    def get(self, request, *args, **kwargs):
        services = Service.objects.all()
        serialized_services = ServiceSerializer(services, many=True).data
        return render(request, 'services/services.html', {'services': serialized_services})
    
def add_services(request):
    if request.method == 'POST':
        form = ServicesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('services')
    else:
        form = ServicesForm()
    
    return render(request, 'services/add-services.html', {'form': form, 'is_edit':False})

def add_service_type(request):
    if request.method == 'POST':
        form = ServiceTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_settings')
    else:
        form = ServiceTypeForm()
    
    return render(request, 'services/add-service-type.html', {'form': form, 'is_edit':False})

def edit_services(request, service_id):
    service = get_object_or_404(Service, service_id=service_id)
    if request.method == 'POST':
        form = ServicesForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services')
    else:
        form = ServicesForm(instance=service)
    
    return render(request, 'services/add-services.html', {'form': form, 'service': service, 'is_edit':True})

class ParkingsListView(View):
    def get(self, request, *args, **kwargs):
        parkings = ParkingSpace.objects.all()
        serialized_parkings = ParkingSerializer(parkings, many=True).data
        return render(request, 'services/parking.html', {'parkings': serialized_parkings})
    
def add_parkings(request):
    if request.method == 'POST':
        form = ParkingSpaceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('parkings')
    else:
        form = ParkingSpaceForm()
    
    return render(request, 'services/add-parking.html', {'form': form, 'is_edit':False})

def book_parkings(request, parking_id):
    parking = get_object_or_404(ParkingSpace, parking_id=parking_id)
    user_id = request.session['user_id']
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = ParkingForm(request.POST)
        if form.is_valid():
            parking.vehicle_number = form.cleaned_data.get('vehicle_number')
            parking.contact_number = form.cleaned_data.get('contact_number')
            parking.is_booked = True
            parking.user = user
            parking.save()
            return redirect('parkings')
    else:
        form = ParkingForm()
    
    return render(request, 'services/add-parking.html', {'form': form, 'is_edit':True, 'id':parking_id})

def cancel_parkings(request, parking_id):
    parking = get_object_or_404(ParkingSpace, parking_id=parking_id)
    parking.vehicle_number = None
    parking.contact_number = None
    parking.is_booked = False
    parking.user = None
    parking.save()
    return redirect('parkings')

class MenuListView(View):
    def get(self, request, *args, **kwargs):
        foods = Menu.objects.filter(type='food')
        serialized_foods = MenuSerializer(foods, many=True).data
        menu = Menu.objects.filter(type='beverages')
        serialized_menu = MenuSerializer(menu, many=True).data
        return render(request, 'services/menu.html', {'foods': serialized_foods,'items': serialized_menu})
    
def add_menu(request):
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = MenuForm()
    
    return render(request, 'services/add-menu.html', {'form': form})