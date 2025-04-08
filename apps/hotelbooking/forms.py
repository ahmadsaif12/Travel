from django import forms
from .models import HotelRoom, HotelRevenue, HotelAmenities, RoomAvailability, HotelBooking
from django.contrib.auth.models import User

# Hotel Booking Form
class HotelBookingForm(forms.ModelForm):
    class Meta:
        model = HotelBooking
        fields = ['hotel_name', 'amount', 'room_type', 'photo', 'hotel_address', 
                  'contact_number', 'total_person', 'arrive_time', 'checkout_time', 
                  'rooms_available', 'total_price', 'location', 'latitude', 'longitude', 'email']

# Hotel Room Form
class HotelRoomForm(forms.ModelForm):
    class Meta:
        model = HotelRoom
        fields = '__all__'

# Hotel Revenue Filter/Edit Form
class HotelRevenueFilterForm(forms.ModelForm):
    class Meta:
        model = HotelRevenue
        fields = '__all__'

# Hotel Amenities Form
class HotelAmenitiesForm(forms.ModelForm):
    class Meta:
        model = HotelAmenities
        fields = '__all__'

# Room Availability Form
class RoomAvailabilityForm(forms.ModelForm):
    class Meta:
        model = RoomAvailability
        fields = '__all__'

# Hotel Login Form
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise ValidationError('Username does not exist.')
        return username