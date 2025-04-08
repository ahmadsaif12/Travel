from django.contrib import admin
from .models import HotelBooking, HotelRoom, HotelRevenue, HotelAmenities, RoomAvailability

# Registering the models in the Django admin site
admin.site.register(HotelBooking)
admin.site.register(HotelRoom)
admin.site.register(HotelRevenue)
admin.site.register(HotelAmenities)  # Added HotelAmenities model
admin.site.register(RoomAvailability)  # Added RoomAvailability model
