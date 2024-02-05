from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from hotel.user.models import Customer
from hotel.services.models import ServiceType
from hotel.services.serializers import ServiceTypeSerializer
from .models import Room, RoomRate, Amenities, RoomType, AmenityType
from .serializers import *
from .forms import *
from django.http import JsonResponse, HttpResponseForbidden
from datetime import datetime
import json

def home(request):
    if request.method == 'POST':
        rooms = None
        form = RoomSearchForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            guests = form.cleaned_data['adults_count']
            rooms = Room.objects.filter(max_capacity__gt=guests)
            serialized_rooms = RoomSerializer(rooms, many=True, start_date=start_date, end_date=end_date).data
            return render(request, 'rooms.html', {'rooms': serialized_rooms, 'form': form}) 
    else:
        form = RoomSearchForm()
        rooms = Room.objects.all()
        serialized_rooms = RoomSerializer(rooms, many=True).data

    return render(request, 'home.html', {'rooms': serialized_rooms, 'form': form})  

def add_rooms(request):
    if request.method == 'POST':
        room_form = RoomForm(request.POST)
        image_form = RoomImageForm(request.POST, request.FILES, prefix='image')
        if room_form.is_valid() and image_form.is_valid():
            room = room_form.save()
            # Associate the room with images
            for image in request.FILES.getlist('image-image'):
                RoomImage.objects.create(room=room, image=image)
            return redirect('rooms')
    else:
        room_form = RoomForm()
        image_form = RoomImageForm(prefix='image')

    return render(request, 'add-room.html', {'form': room_form, 'image_form': image_form, 'is_edit': False})

def edit_room(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    if request.method == 'POST':
        room_form = RoomForm(request.POST, instance=room)
        image_form = RoomImageForm(request.POST, request.FILES, prefix='image')
        if room_form.is_valid() and image_form.is_valid():
            room = room_form.save()
            # Clear existing images associated with the room and associate the new ones
            room.roomimage_set.all().delete()
            for image in request.FILES.getlist('image-image'):
                RoomImage.objects.create(room=room, image=image)
            return redirect('rooms')
    else:
        room_form = RoomForm(instance=room)
        image_form = RoomImageForm(prefix='image')

    return render(request, 'add-room.html', {'form': room_form, 'image_form': image_form, 'room': room, 'is_edit': True})


def rooms_list(request):
    if request.method == 'POST':
        rooms = None
        form = RoomSearchForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            guests = form.cleaned_data['adults_count']
            date_difference = end_date - start_date
            number_of_days = date_difference.days
            rooms = Room.objects.filter(max_capacity__gt=guests)
            serialized_rooms = RoomSerializer(rooms, many=True, start_date=start_date, end_date=end_date, days=number_of_days).data
    else:
        form = RoomSearchForm()
        rooms = Room.objects.filter(max_capacity__gt=2)
        serialized_rooms = RoomSerializer(rooms, many=True).data

    return render(request, 'rooms.html', {'rooms': serialized_rooms, 'form': form})  
    

def room_details(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    amenity_types = Amenities.objects.filter(room_reference__room_number=room_number).values('type__name').distinct()
    last_4_reviews = Rating.objects.filter(booking_reference__room__room_number=room_number)
    
    # Query room images associated with the room
    room_images = RoomImage.objects.filter(room=room)
    
    # Serialize the room
    serialized_room = RoomSerializer(room).data

    return render(request, 'room.html', {
        'room': serialized_room,
        'amenities': amenity_types,
        'reviews': last_4_reviews,
        'room_images': room_images,
    })

def add_room_rate(request):
    if request.method == 'POST':
        form = RoomRateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('rooms')
    else:
        form = RoomRateForm()
    
    return render(request, 'add-room-rate.html', {'form': form})
    
def room_rates_list(request):
    rates = RoomRate.objects.all()
    serialized_rates = RoomRateSerializer(rates, many=True).data
    return render(request, 'room-rates.html', {'rates': serialized_rates})

    
class AmenitiesListView(View):
    def get(self, request, *args, **kwargs):
        if request.session.get('access_type', 'Customer') not in ['Admin', 'Owner']:
            return HttpResponseForbidden("Access Denied.")
        amenities = Amenities.objects.all()
        serialized_amenities = AmenitiesSerializer(amenities, many=True).data
        return render(request, 'amenities.html', {'amenities': serialized_amenities})
    
def add_amenities(request):
    if request.method == 'POST':
        form = AmenitiesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('amenities')
    else:
        form = AmenitiesForm()
    
    return render(request, 'add-amenities.html', {'form': form, 'is_edit':False})

def edit_amenities(request, amenity_id):
    amenity = get_object_or_404(Amenities, id=amenity_id)
    if request.method == 'POST':
        form = AmenitiesForm(request.POST, instance=amenity)
        if form.is_valid():
            form.save()
            return redirect('amenities')
    else:
        form = AmenitiesForm(instance=amenity)
    
    return render(request, 'add-amenities.html', {'form': form, 'amenity': amenity, 'is_edit':True})


def get_amenity(request, amenity_id):
    try:
        amenity = Amenities.objects.get(pk=amenity_id)
        amenity_data = {
            'type': amenity.type,
            'purchase_amount': amenity.purchase_amount,
            'status': amenity.status,
        }

        room_reference_data = {
            'id': amenity.room_reference.id,
            'name': amenity.room_reference.room_number,
        }

        amenity_data['room_reference'] = room_reference_data

        return JsonResponse(amenity_data)
    except Amenities.DoesNotExist:
        return JsonResponse({'error': f'Amenity with ID {amenity_id} not found'}, status=404)
    
def room_settings(request):
    room_types = RoomType.objects.all()
    amenity_types = AmenityType.objects.all()
    service_types = ServiceType.objects.all()
    serialized_room_types = RoomTypeSerializer(room_types, many=True).data
    serialized_amenity_types = AmenityTypeSerializer(amenity_types, many=True).data
    serialized_service_types = ServiceTypeSerializer(service_types, many=True).data
    return render(request, 'room-settings.html', {'room_types': serialized_room_types,
                                                  'service_types': serialized_service_types,
                                                  'amenity_types': serialized_amenity_types})


def get_rooms(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            adults_count = int(data.get('adultsCount'))
            max_capacity = int(data.get('maxCapacity'))
            single_room = Room.objects.filter(max_capacity__gte=adults_count).first()
            print(adults_count)
            mutliple_room = Room.objects.filter(max_capacity__gte=adults_count).first()
            return JsonResponse({'single_room': RoomSerializer(single_room).data if single_room else None,
                                 'mutliple_room': RoomSerializer(mutliple_room).data if mutliple_room else None})
        except ValueError:
            return JsonResponse({'message': 'Invalid input for adults count.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

def add_room_type(request):
    if request.method == 'POST':
        form = RoomTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_settings')
    else:
        form = RoomTypeForm()
    
    return render(request, 'add-room-type.html', {'form': form, 'is_edit':False})

def add_aminity_type(request):
    if request.method == 'POST':
        form = AmenityTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('room_settings')
    else:
        form = AmenityTypeForm()
    
    return render(request, 'add-aminity-type.html', {'form': form, 'is_edit':False})

def book_room(request, room_number):
    standard_room_rate = 1000
    room_details = {'amenities':[]}
    user = None
    logged_in = request.session.get('logged_in', False)
    if not logged_in:
        return redirect('login')
    user_id = request.session['user_id']
    user = get_object_or_404(User, id=user_id)
    try:
        customer = Customer.objects.get(user__id=user_id)
    except ObjectDoesNotExist:
        customer = None
    room = get_object_or_404(Room, room_number=room_number)
    amenity_types = Amenities.objects.filter(room_reference__room_number=room_number).values('type__name').distinct()
    for amenity in amenity_types:
        room_details['amenities'].append(amenity['type__name']) 
    print("...........................", request.POST)
    if request.method == 'POST':
        booking_form = BookingForm(request.POST, room=room)
        if booking_form.is_valid():
            check_in_date = booking_form.cleaned_data['check_in_date']
            check_out_date = booking_form.cleaned_data['check_out_date']
            number_of_days = (check_out_date - check_in_date).days
            last_room_rate_for_room = RoomRate.objects.filter(
                room_reference=room,
                date__range=(check_in_date, check_out_date),
                is_available=True,
                is_active=True
            ).order_by('-date').first()
            amount = last_room_rate_for_room.amount if last_room_rate_for_room else standard_room_rate
            selected_room_numbers = booking_form.cleaned_data.get('selected_rooms').split(',')
            selected_rooms = Room.objects.filter(room_number__in=selected_room_numbers)
            selected_rooms = list(selected_rooms)
            selected_rooms.append(room)
            print(selected_rooms,"...........................")
            booking_data = {
                'customer': customer,
                'user': user,
                'amount': amount,
                'booking_date': datetime.now(),
                'check_in_date': check_in_date,
                'check_out_date': check_out_date,
                'number_of_days': number_of_days,
                'status': 'Reservation',
            }
            booking = Booking(**booking_data)
            booking.save()
            # Use the .set() method to assign the selected rooms to the booking
            booking.room.set(selected_rooms)
            return redirect('my_bookings')
        else:
            print("......................invalid............................")
            print("Form is invalid. Errors:")
            for field, errors in booking_form.errors.items():
                print(f"Field: {field}, Errors: {', '.join(errors)}")

    else:
        booking_form = BookingForm(room=room)
    room_details.update(RoomSerializer(room).data)
    return render(request, 'book-room.html', {'booking_form': booking_form,
                                              'room':room_details})

def payment(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            paid_amount = payment_form.cleaned_data['amount']
            payment_data = {
                'payment_date': datetime.now(),
                'booking_reference': booking,
                'amount': paid_amount,
                'payment_type': 'Completed' if paid_amount >= booking.amount else 'Pending',
                'payment_type': payment_form.cleaned_data['payment_type'],
            }
            payment = Payment(**payment_data)
            payment.save()
            return redirect('my_bookings')
    else:
        initial_data = {
            'amount': booking.amount,
        }
        payment_form = PaymentForm(initial=initial_data)
    
    return render(request, 'payment.html', {'payment_form': payment_form})

class BookingsListView(View):
    def get(self, request, *args, **kwargs):
        if request.session.get('access_type', 'Customer') not in ['Admin', 'Owner']:
            return HttpResponseForbidden("Access Denied.")
        bookings = Booking.objects.all()
        serialized_bookings = BookingSerializer(bookings, many=True).data
        return render(request, 'bookings.html', {'bookings': serialized_bookings})
    
class MyBookingsListView(View):
    def get(self, request, *args, **kwargs):
        user_id = request.session['user_id']
        bookings = Booking.objects.filter(user_id=user_id)
        serialized_bookings = BookingSerializer(bookings, many=True).data
        return render(request, 'my-bookings.html', {'bookings': serialized_bookings})
    
def booking_details(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    serialized_booking = BookingSerializer(booking).data
    return render(request, 'booking.html', {'booking_data': serialized_booking})

def update_bookings(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    if booking.status == 'Reservation':
        booking.status = 'CheckedIn'
    elif booking.status == 'CheckedIn':
        booking.status = 'CheckedOut'
    booking.save()
    return redirect('my_bookings')

def cancel_bookings(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    if request.method == 'POST':
        booking.status = 'Canceled'
        booking.save()
        serialized_booking = BookingSerializer(booking).data
        refund_amount = calculate_refund_amount(booking.check_in_date, booking.amount)
        response_data = {
            'booking_id': booking.booking_id,
            'refund_amount': refund_amount,
        }
        return JsonResponse(response_data)
    else:
        serialized_booking = BookingSerializer(booking).data
        print(serialized_booking)
        return render(request, 'cancel-booking.html', {'booking_data': serialized_booking})

def calculate_refund_amount(check_in_date, total_amount):
    # Assume cancellation policies
    cancellation_policy_1_days = 7
    cancellation_policy_2_days = 2

    total_amount = float(total_amount)

    # Calculate the difference between check-in date and current date
    days_until_check_in = (check_in_date - datetime.now().date()).days

    # Apply cancellation policies
    if days_until_check_in > cancellation_policy_1_days:
        # Cancelation before 7 days: No charge
        refund_amount = total_amount
    elif cancellation_policy_2_days <= days_until_check_in <= cancellation_policy_1_days:
        # Cancelation within 7-2 days: 50% of booking fee
        refund_amount = total_amount * 0.5
    else:
        # Cancelation within 2 days of check-in: 90% of booking fee
        refund_amount = total_amount * 0.9

    return round(refund_amount, 2)  # Round to 2 decimal places

def cancel_room_bookings(request, booking_id, room_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    canceled_rooms = booking.canceled_rooms or ''
    canceled_rooms += f"{room_id},"
    booking.canceled_rooms = canceled_rooms
    booking.save()
    latest_rate = RoomRate.objects.filter(room_reference__room_number=room_id).latest('date')
    refund_amount = float(latest_rate.amount) * float(0.5)
    response_data = {
            'refund_amount': refund_amount,
        }
    return JsonResponse(response_data)

def rate_bookings(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    try:
        rating = Rating.objects.get(booking_reference=booking)
        print(rating)
        return HttpResponseForbidden("Expired.")
    except Rating.DoesNotExist:
        print("New Rating")
    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating_instance = form.save(commit=False)
            rating_instance.booking_reference = booking
            rating_instance.save()
            form.save_m2m()
            redirect('my_bookings')
    else:
        form = RatingForm()

    context = {
        'form': form,
        'booking': BookingSerializer(booking).data
    }

    return render(request, 'rating.html', context)