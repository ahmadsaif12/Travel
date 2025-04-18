from django.shortcuts import render, redirect, get_object_or_404
from .models import HotelBooking, HotelRoom, HotelRevenue, HotelAmenities, RoomAvailability
from .forms import HotelBookingForm, HotelRoomForm, HotelRevenueFilterForm, HotelAmenitiesForm, RoomAvailabilityForm, LoginForm
from django.db.models import Sum, Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

#-----------------------------------------------------

def view_hotel_room(request, room_id):
    room = get_object_or_404(HotelRoom, id=room_id)
    return render(request, 'hotel_booking/view_hotel_room.html', {'room': room})

# Hotel Revenue List
def hotel_revenue_list(request):
    query = request.GET.get('q', '')
    revenues = HotelRevenue.objects.all()

    if query:
        revenues = revenues.filter(
            Q(hotel_name__icontains=query) | Q(status__icontains=query)
        )

    total_revenue = revenues.aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0

    return render(request, 'hotel_booking/hotel_revenue_list.html', {
        'revenues': revenues,
        'total_revenue': total_revenue,
        'query': query,
    })

# List all hotel rooms
def hotel_rooms_list(request):
    rooms = HotelRoom.objects.all()
    room_count = rooms.count()
    return render(request, 'hotel_booking/hotel_rooms.html', {'rooms': rooms, 'room_count': room_count})

# Add a new hotel room
def add_hotel_room(request):
    if request.method == 'POST':
        hotel_id = request.POST.get('hotel_id')
        hotel = get_object_or_404(HotelBooking, id=hotel_id)

        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        status = request.POST.get('status')
        price_per_night = request.POST.get('price_per_night')
        description = request.POST.get('description')

        room = HotelRoom(
            hotel=hotel,
            room_number=room_number,
            room_type=room_type,
            status=status,
            price_per_night=price_per_night,
            description=description
        )
        room.save()

        return redirect('hotel_rooms_list')

    hotels = HotelBooking.objects.all()
    return render(request, 'hotel_booking/add_hotel_room.html', {'hotels': hotels})

# Edit an existing hotel room
def edit_hotel_room(request, room_id):
    room = get_object_or_404(HotelRoom, id=room_id)

    if request.method == 'POST':
        room.room_number = request.POST.get('room_number')
        room.room_type = request.POST.get('room_type')
        room.status = request.POST.get('status')
        room.price_per_night = request.POST.get('price_per_night')
        room.description = request.POST.get('description')
        room.save()
        return redirect('hotel_rooms_list')

    return render(request, 'hotel_booking/edit_hotel_room.html', {'room': room})

# Delete a hotel room
def delete_hotel_room(request, room_id):
    room = get_object_or_404(HotelRoom, id=room_id)
    room.delete()
    return redirect('hotel_rooms_list')

# List all hotel bookings with search & filter
def hotel_booking_list(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status')

    bookings = HotelBooking.objects.all()

    if query:
        bookings = bookings.filter(hotel_name__icontains=query)
    if status_filter:
        bookings = bookings.filter(status=status_filter)

    return render(request, 'hotel_booking/hotel_booking_list.html', {'bookings': bookings})

# Hotel Dashboard
def hotel_login_view(request):
    if request.user.is_authenticated:
        return redirect('hotel_dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('hotel_dashboard')
            else:
                return render(request, 'hotel_login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    
    return render(request, 'hotel_booking/hotel_login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('hotel_login')

# Hotel Dashboard
@login_required(login_url='hotel_login/') 
def hotel_dashboard(request):
    total_bookings = HotelBooking.objects.count()
    total_revenue = sum(b.total_price for b in HotelBooking.objects.all())
    available_rooms = HotelRoom.objects.filter(status='Available')
    hotels = HotelBooking.objects.all()
    total_amenities = HotelAmenities.objects.count()
    total_room_availability = RoomAvailability.objects.count()
    hotel_name = "Your Hotel Name"

    context = {
        'total_bookings': total_bookings,
        'total_revenue': total_revenue,
        'available_rooms': available_rooms,
        'hotels': hotels,
        'total_amenities': total_amenities,
        'total_room_availability': total_room_availability,
        'hotel_name': hotel_name,
    }

    return render(request, 'hotel_booking/hotel_dashboard.html', context)

def view_hotel_revenue(request, revenue_id):
    revenue = get_object_or_404(HotelRevenue, id=revenue_id)
    return render(request, 'hotel_booking/view_hotel_revenue.html', {'revenue': revenue})

# Edit hotel revenue
def edit_hotel_revenue(request, revenue_id):
    revenue = get_object_or_404(HotelRevenue, id=revenue_id)
    
    if request.method == 'POST':
        form = HotelRevenueFilterForm(request.POST, instance=revenue)
        if form.is_valid():
            form.save()
            return redirect('hotel_booking/hotel_revenue_list')
    else:
        form = HotelRevenueFilterForm(instance=revenue)

    return render(request, 'hotel_booking/edit_hotel_revenue.html', {'form': form, 'revenue': revenue})

# Delete hotel revenue
def delete_hotel_revenue(request, revenue_id):
    revenue = get_object_or_404(HotelRevenue, id=revenue_id)
    revenue.delete()
    return redirect('hotel_booking/hotel_revenue_list')

# Add a new hotel booking
def add_hotel_booking(request):
    if request.method == "POST":
        form = HotelBookingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('hotel_booking_list')
    else:
        form = HotelBookingForm()
    return render(request, 'hotel_booking/add_hotel_booking.html', {'form': form})

# Edit a hotel booking
def edit_hotel_booking(request, hotel_id):
    booking = get_object_or_404(HotelBooking, hotel_id=hotel_id)
    if request.method == "POST":
        form = HotelBookingForm(request.POST, request.FILES, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('hotel_booking_list')
    else:
        form = HotelBookingForm(instance=booking)
    return render(request, 'hotel_booking/edit_hotel_booking.html', {'form': form})

# Delete a hotel booking
def delete_hotel_booking(request, hotel_id):
    booking = get_object_or_404(HotelBooking, hotel_id=hotel_id)
    booking.delete()
    return redirect('hotel_booking_list')

# Add Amenity
def add_hotel_amenity(request, hotel_id):
    hotel = get_object_or_404(HotelBooking, pk=hotel_id)
    if request.method == 'POST':
        form = HotelAmenitiesForm(request.POST)
        if form.is_valid():
            amenity = form.save(commit=False)
            amenity.hotel = hotel
            amenity.save()
            return redirect('hotel_dashboard')
    else:
        form = HotelAmenitiesForm()
    return render(request, 'hotel_booking/add_hotel_amenity.html', {'form': form, 'hotel': hotel})

# Edit Amenity
def edit_hotel_amenity(request, id):
    amenity = get_object_or_404(HotelAmenities, id=id)
    if request.method == 'POST':
        form = HotelAmenitiesForm(request.POST, instance=amenity)
        if form.is_valid():
            form.save()
            return redirect('amenity-list')
    else:
        form = HotelAmenitiesForm(instance=amenity)
    
    return render(request, 'hotel_booking/edit_hotel_amenity.html', {'form': form, 'amenity': amenity})

def delete_hotel_amenity(request, id):
    amenity = get_object_or_404(HotelAmenities, id=id)
    amenity.delete()
    return redirect('amenity-list')

# Add Room Availability
def add_room_availability(request, room_id):
    room = get_object_or_404(HotelRoom, id=room_id)
    if request.method == 'POST':
        form = RoomAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.room = room
            availability.save()
            return redirect('room-availability-list')
    else:
        form = RoomAvailabilityForm()

    return render(request, 'hotel_booking/add_room_availability.html', {'form': form, 'room': room})

def edit_availability(request, pk):
    availability = get_object_or_404(RoomAvailability, pk=pk)
    if request.method == 'POST':
        form = RoomAvailabilityForm(request.POST, instance=availability)
        if form.is_valid():
            form.save()
            return redirect('hotel_dashboard')
    else:
        form = RoomAvailabilityForm(instance=availability)
    return render(request, 'hotel_booking/edit_room_availability.html', {'form': form})

# Delete Room Availability
def delete_availability(request, pk):
    availability = get_object_or_404(RoomAvailability, pk=pk)
    availability.delete()
    return redirect('hotel_dashboard')

def amenity_list(request):
    amenities = HotelAmenities.objects.select_related('hotel').all()
    return render(request, 'hotel_booking/amenity_list.html', {'amenities': amenities})

def room_availability_list(request):
    availability_list = RoomAvailability.objects.select_related('room__hotel').all()
    hotel_id = None
    if availability_list:
        first_availability = availability_list.first()
        if first_availability.room and first_availability.room.hotel:
            hotel_id = first_availability.room.hotel.hotel_id

    return render(request, 'hotel_booking/room_availability_list.html', {
        'availability_list': availability_list,
        'hotel_id': hotel_id,
    })

def view_hotel_amenity(request, hotel_id):
    hotel = get_object_or_404(HotelBooking, pk=hotel_id)
    amenities = HotelAmenities.objects.filter(hotel=hotel)
    return render(request, 'hotel_booking/view_hotel_amenity.html', {
        'hotel': hotel,
        'amenities': amenities,
    })

def view_room_availability(request, hotel_id):
    hotel = get_object_or_404(HotelBooking, pk=hotel_id)
    rooms = hotel.rooms.all()
    room_availabilities = RoomAvailability.objects.filter(room__in=rooms)
    return render(request, 'hotel_booking/view_room_availability.html', {
        'hotel': hotel,
        'room_availabilities': room_availabilities,
    })
