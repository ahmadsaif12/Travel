from django.db import models
from django.contrib.auth.models import User
from apps.maps.models import Location

class HotelBooking(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    room_type = models.CharField(max_length=20)
    photo = models.ImageField(upload_to="hotel_photos/", null=True, blank=True)
    hotel_address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    total_person = models.IntegerField()
    arrive_time = models.DateTimeField()
    checkout_time = models.DateTimeField()
    rooms_available = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return f"Hotel Booking at {self.hotel_name} - {self.user.username}"

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than 0")

        # Additional validation for room count vs availability
        if self.total_person > self.rooms_available:
            raise ValidationError("Total persons cannot exceed available rooms.")


class HotelRoom(models.Model):
    ROOM_TYPE_CHOICES = [
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
        ('Standard', 'Standard'),
    ]

    room_number = models.CharField(max_length=100)
    room_type = models.CharField(max_length=100, choices=ROOM_TYPE_CHOICES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    status = models.CharField(
        max_length=50,
        choices=[('Available', 'Available'), ('Booked', 'Booked'), ('Occupied', 'Occupied')],
        default='Available'
    )
    hotel = models.ForeignKey('HotelBooking', on_delete=models.CASCADE, related_name='rooms')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return f"Room {self.room_number} ({self.room_type})"

    def clean(self):
        # Additional validation for price
        if self.price_per_night <= 0:
            raise ValidationError("Price per night must be greater than 0.")


# Model to track hotel amenities (WiFi, AC, Breakfast, etc.)
# models.py

class HotelAmenities(models.Model):
    AMENITY_CHOICES = [
        ('wifi', 'WiFi'),
        ('ac', 'Air Conditioning'),
        ('breakfast', 'Breakfast'),
        ('pool', 'Swimming Pool'),
        ('parking', 'Parking'),
        ('gym', 'Gym'),
        ('spa', 'Spa'),
        ('tv', 'Television'),
        ('minibar', 'Minibar'),
    ]

    hotel = models.ForeignKey('HotelBooking', on_delete=models.CASCADE, related_name='amenities')
    amenity = models.CharField(max_length=100, choices=AMENITY_CHOICES)

    def __str__(self):
        return f"{self.get_amenity_display()} at {self.hotel.hotel_name}"



# Room Availability model to track availability per date
class RoomAvailability(models.Model):
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, related_name='availabilities')
    available_date = models.DateField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Availability for Room {self.room.room_number} on {self.available_date}"

    def clean(self):
        # Ensure availability date is in the future
        if self.available_date < models.DateField.today():
            raise ValidationError("Availability date cannot be in the past.")


# Revenue model to track hotel revenue
class HotelRevenue(models.Model):
    hotel_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Revenue for {self.hotel_name}: {self.amount}"
