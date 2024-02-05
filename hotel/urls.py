"""
URL configuration for hotel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views
from hotel.user import views as user_views
from hotel.room import views as room_views
from hotel.services import views as service_views

urlpatterns = [
    path('', room_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('users/', user_views.UserList.as_view(), name='users'),
    path('signup/', csrf_exempt(user_views.customer_signup), name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('rooms/', room_views.rooms_list, name='rooms'),
    path('rooms/add/', room_views.add_rooms, name='add_room'),
    path('rooms/<int:room_number>/edit/', room_views.edit_room, name='edit_room'),
    path('rooms/<int:room_number>/', room_views.room_details, name='room_details'),
    path('rooms/<int:room_number>/book/', room_views.book_room, name='book_room'),
    path('rooms/<int:booking_id>/pay/', room_views.payment, name='payment'),
    path('rooms/rates/add/', room_views.add_room_rate, name='add_room_rate'),
    path('rooms/types/add/', room_views.add_room_type, name='add_room_type'),
    path('rooms/rates/', room_views.room_rates_list, name='room_rates'),
    path('rooms/settings/', room_views.room_settings, name='room_settings'),
    path('get-rooms/', csrf_exempt(room_views.get_rooms), name='get_rooms'),
    path('bookings/', room_views.BookingsListView.as_view(), name='bookings'),
    path('booking/<int:booking_id>/', room_views.booking_details, name='booking_details'),
    path('booking/<int:booking_id>/update/', room_views.update_bookings, name='update_bookings'),
    path('booking/<int:booking_id>/cancel/', csrf_exempt(room_views.cancel_bookings), name='cancel_bookings'),
    path('booking/<int:booking_id>/room/<int:room_id>/cancel/', csrf_exempt(room_views.cancel_room_bookings), name='cancel_bookings'),
    path('booking/<int:booking_id>/rate/', room_views.rate_bookings, name='rate_bookings'),
    path('my-bookings/', room_views.MyBookingsListView.as_view(), name='my_bookings'),
    path('amenities/', room_views.AmenitiesListView.as_view(), name='amenities'),
    path('amenities/add/', room_views.add_amenities, name='add_amenities'),
    path('amenities/types/add/', room_views.add_aminity_type, name='add_aminity_type'),
    path('amenities/<int:amenity_id>/get/', room_views.get_amenity, name='get_amenity'),
    path('amenities/<int:amenity_id>/edit/', csrf_exempt(room_views.edit_amenities), name='edit_amenities'),
    path('services/', service_views.ServicesListView.as_view(), name='services'),
    path('services/add/', service_views.add_services, name='add_services'),
    path('services/<int:service_id>/edit/', service_views.edit_services, name='edit_services'),
    path('services/types/add/', service_views.add_service_type, name='add_service_type'),
    path('menu/', service_views.MenuListView.as_view(), name='menu'),
    path('menu/add/', service_views.add_menu, name='add_menu'),
    path('parkings/', service_views.ParkingsListView.as_view(), name='parkings'),
    path('parkings/add/', service_views.add_parkings, name='add_parkings'),
    path('parkings/<int:parking_id>/book/', service_views.book_parkings, name='book_parkings'),
    path('parkings/<int:parking_id>/cancel/', service_views.cancel_parkings, name='cancel_parkings'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)