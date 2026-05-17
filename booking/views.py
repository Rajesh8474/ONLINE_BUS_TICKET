import json
import random
import string
import time
from datetime import datetime, date

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt

from .models import User, Bus, BusReview, Booking, Passenger, AdminUser


# ─── Helpers ─────────────────────────────────────────────────────────────────

def health(request):
    return HttpResponse("OK")

def generate_booking_id():
    ts = str(int(time.time() * 1000))[-8:]
    rnd = str(random.randint(10, 99))
    return 'BK' + ts + rnd


def get_session_user(request):
    uid = request.session.get('user_id')
    if uid:
        try:
            return User.objects.get(id=uid)
        except User.DoesNotExist:
            pass
    return None


def is_admin_session(request):
    return request.session.get('admin_logged_in', False)


def format_date(d):
    """Format a date object or ISO string for display."""
    if isinstance(d, str):
        try:
            d = datetime.strptime(d, '%Y-%m-%d').date()
        except Exception:
            return d
    return d.strftime('%-d %b %Y')


# ─── Seed Data ────────────────────────────────────────────────────────────────

def seed_data():
    """Called once to seed buses and admin if DB is empty."""
    if not Bus.objects.exists():
        buses_data = [
            {
                'bus_id': 'bus001', 'name': 'Rajdhani Express', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Kolkata',
                'departure': '06:00', 'arrival': '12:30', 'duration': '6h 30m',
                'price': 650, 'total_seats': 40, 'rating': 4.3,
                'amenities': ['WiFi', 'Charging Point', 'Blanket'],
                'boarding_points': ['Bhubaneswar ISBT', 'Cuttack Bus Stand'],
                'dropping_points': ['Kharagpur', 'Kolkata Esplanade'],
                'reviews': [
                    {'user_name': 'Rahul M', 'comment': 'Good service, AC was nice', 'stars': 4},
                    {'user_name': 'Priya S', 'comment': 'On time departure', 'stars': 5},
                ],
            },
            {
                'bus_id': 'bus002', 'name': 'Konark Travels', 'operator': 'Private',
                'bus_type': 'Sleeper', 'from_city': 'Bhubaneswar', 'to_city': 'Kolkata',
                'departure': '21:00', 'arrival': '05:00', 'duration': '8h 00m',
                'price': 850, 'total_seats': 30, 'rating': 4.1,
                'amenities': ['Blanket', 'Pillow', 'Charging Point'],
                'boarding_points': ['Bhubaneswar ISBT', 'Patia'],
                'dropping_points': ['Kolkata Ultadanga', 'Kolkata Esplanade'],
                'reviews': [
                    {'user_name': 'Amit K', 'comment': 'Comfortable sleeper journey', 'stars': 4},
                ],
            },
            {
                'bus_id': 'bus003', 'name': 'Eastern Deluxe', 'operator': 'Greenline',
                'bus_type': 'Non-AC', 'from_city': 'Bhubaneswar', 'to_city': 'Kolkata',
                'departure': '08:30', 'arrival': '16:00', 'duration': '7h 30m',
                'price': 350, 'total_seats': 45, 'rating': 3.8,
                'amenities': ['Charging Point'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Kolkata Esplanade', 'Kolkata Howrah'],
                'reviews': [],
            },
            {
                'bus_id': 'bus004', 'name': 'Puri Special', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Puri',
                'departure': '07:00', 'arrival': '09:00', 'duration': '2h 00m',
                'price': 180, 'total_seats': 40, 'rating': 4.5,
                'amenities': ['WiFi', 'Charging Point'],
                'boarding_points': ['Bhubaneswar ISBT', 'Vani Vihar'],
                'dropping_points': ['Puri Bus Stand', 'Puri Beach Road'],
                'reviews': [
                    {'user_name': 'Sneha P', 'comment': 'Quick and comfortable', 'stars': 5},
                ],
            },
            {
                'bus_id': 'bus005', 'name': 'Visakha Express', 'operator': 'APSRTC',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Visakhapatnam',
                'departure': '22:00', 'arrival': '06:30', 'duration': '8h 30m',
                'price': 750, 'total_seats': 40, 'rating': 4.2,
                'amenities': ['WiFi', 'Charging Point', 'Blanket'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Visakhapatnam RTC Complex', 'Dwaraka Nagar'],
                'reviews': [],
            },
            {
                'bus_id': 'bus006', 'name': 'Capital Cruiser', 'operator': 'Sharma Travels',
                'bus_type': 'Sleeper', 'from_city': 'Kolkata', 'to_city': 'Bhubaneswar',
                'departure': '20:30', 'arrival': '04:30', 'duration': '8h 00m',
                'price': 900, 'total_seats': 30, 'rating': 4.0,
                'amenities': ['Blanket', 'Pillow', 'Charging Point'],
                'boarding_points': ['Kolkata Esplanade', 'Kolkata Ultadanga'],
                'dropping_points': ['Bhubaneswar ISBT', 'Patia'],
                'reviews': [],
            },
    # ================= ODISHA (60) =================
            {
                'bus_id': 'bus007', 'name': 'Utkal Express', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Cuttack',
                'departure': '09:00', 'arrival': '10:30', 'duration': '1h 30m',
                'price': 120, 'total_seats': 40, 'rating': 4.2,
                'amenities': ['WiFi', 'Charging Point'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Cuttack Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus008', 'name': 'Jagannath Rider', 'operator': 'Private',
                'bus_type': 'Sleeper', 'from_city': 'Bhubaneswar', 'to_city': 'Berhampur',
                'departure': '22:00', 'arrival': '04:00', 'duration': '6h 00m',
                'price': 500, 'total_seats': 30, 'rating': 4.0,
                'amenities': ['Blanket', 'Charging Point'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Berhampur Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus009', 'name': 'Kalinga Express', 'operator': 'OSRTC',
                'bus_type': 'Non-AC', 'from_city': 'Cuttack', 'to_city': 'Puri',
                'departure': '07:30', 'arrival': '10:30', 'duration': '3h 00m',
                'price': 150, 'total_seats': 45, 'rating': 3.9,
                'amenities': ['Charging Point'],
                'boarding_points': ['Cuttack Bus Stand'],
                'dropping_points': ['Puri Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus010', 'name': 'Sambalpur Deluxe', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Sambalpur',
                'departure': '06:30', 'arrival': '13:30', 'duration': '7h 00m',
                'price': 400, 'total_seats': 40, 'rating': 4.1,
                'amenities': ['WiFi', 'Charging Point'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Sambalpur Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus011', 'name': 'Rourkela Rider', 'operator': 'Private',
                'bus_type': 'Sleeper', 'from_city': 'Bhubaneswar', 'to_city': 'Rourkela',
                'departure': '21:30', 'arrival': '06:00', 'duration': '8h 30m',
                'price': 650, 'total_seats': 30, 'rating': 4.2,
                'amenities': ['Blanket', 'Charging Point'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Rourkela Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus012', 'name': 'Balasore Express', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Balasore',
                'departure': '08:00', 'arrival': '12:30', 'duration': '4h 30m',
                'price': 300, 'total_seats': 40, 'rating': 4.0,
                'amenities': ['WiFi'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Balasore Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus025', 'name': 'Balangir Express', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Balangir',
                'departure': '07:30', 'arrival': '15:30', 'duration': '8h 00m',
                'price': 520, 'total_seats': 40, 'rating': 4.1,
                'amenities': ['WiFi', 'Charging Point'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Balangir Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus026', 'name': 'Titlagarh Rider', 'operator': 'Private',
                'bus_type': 'Sleeper', 'from_city': 'Bhubaneswar', 'to_city': 'Titlagarh',
                'departure': '21:00', 'arrival': '06:00', 'duration': '9h 00m',
                'price': 650, 'total_seats': 30, 'rating': 4.2,
                'amenities': ['Blanket', 'Charging Point'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Titlagarh Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus027', 'name': 'Sonepur Express', 'operator': 'OSRTC',
                'bus_type': 'Non-AC', 'from_city': 'Sambalpur', 'to_city': 'Sonepur',
                'departure': '09:00', 'arrival': '12:30', 'duration': '3h 30m',
                'price': 200, 'total_seats': 45, 'rating': 3.9,
                'amenities': ['Charging Point'],
                'boarding_points': ['Sambalpur Bus Stand'],
                'dropping_points': ['Sonepur Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus028', 'name': 'Boudh Express', 'operator': 'Private',
                'bus_type': 'Non-AC', 'from_city': 'Bhubaneswar', 'to_city': 'Boudh',
                'departure': '10:00', 'arrival': '15:00', 'duration': '5h 00m',
                'price': 300, 'total_seats': 45, 'rating': 3.8,
                'amenities': ['Charging Point'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Boudh Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus029', 'name': 'Nuapada Deluxe', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Nuapada',
                'departure': '06:00', 'arrival': '16:00', 'duration': '10h 00m',
                'price': 700, 'total_seats': 40, 'rating': 4.0,
                'amenities': ['WiFi'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Nuapada Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus030', 'name': 'Kendrapara Rider', 'operator': 'Private',
                'bus_type': 'Non-AC', 'from_city': 'Cuttack', 'to_city': 'Kendrapara',
                'departure': '08:30', 'arrival': '11:30', 'duration': '3h 00m',
                'price': 180, 'total_seats': 45, 'rating': 3.9,
                'amenities': ['Charging Point'],
                'boarding_points': ['Cuttack Bus Stand'],
                'dropping_points': ['Kendrapara Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus031', 'name': 'Jagatsinghpur Express', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Jagatsinghpur',
                'departure': '07:00', 'arrival': '09:30', 'duration': '2h 30m',
                'price': 150, 'total_seats': 40, 'rating': 4.1,
                'amenities': ['WiFi'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Jagatsinghpur Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus032', 'name': 'Malkangiri Express', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Berhampur', 'to_city': 'Malkangiri',
                'departure': '06:30', 'arrival': '15:30', 'duration': '9h 00m',
                'price': 650, 'total_seats': 40, 'rating': 4.0,
                'amenities': ['WiFi', 'Charging Point'],
                'boarding_points': ['Berhampur Bus Stand'],
                'dropping_points': ['Malkangiri Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus033', 'name': 'Nabarangpur Rider', 'operator': 'Private',
                'bus_type': 'Sleeper', 'from_city': 'Berhampur', 'to_city': 'Nabarangpur',
                'departure': '21:30', 'arrival': '06:30', 'duration': '9h 00m',
                'price': 680, 'total_seats': 30, 'rating': 4.1,
                'amenities': ['Blanket'],
                'boarding_points': ['Berhampur Bus Stand'],
                'dropping_points': ['Nabarangpur Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus034', 'name': 'Kalahandi Express', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Bhawanipatna',
                'departure': '07:00', 'arrival': '16:00', 'duration': '9h 00m',
                'price': 600, 'total_seats': 40, 'rating': 4.2,
                'amenities': ['WiFi'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Bhawanipatna Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus035', 'name': 'Mayurbhanj Express', 'operator': 'OSRTC',
                'bus_type': 'Non-AC', 'from_city': 'Cuttack', 'to_city': 'Baripada',
                'departure': '08:00', 'arrival': '13:30', 'duration': '5h 30m',
                'price': 280, 'total_seats': 45, 'rating': 3.9,
                'amenities': ['Charging Point'],
                'boarding_points': ['Cuttack Bus Stand'],
                'dropping_points': ['Baripada Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus036', 'name': 'Gopalpur Express', 'operator': 'Private',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Gopalpur',
                'departure': '06:30', 'arrival': '11:30', 'duration': '5h 00m',
                'price': 350, 'total_seats': 40, 'rating': 4.1,
                'amenities': ['WiFi', 'Charging Point'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Gopalpur Beach'],
                'reviews': [],
            },
            {
                'bus_id': 'bus037', 'name': 'Chandipur Express', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Chandipur',
                'departure': '07:00', 'arrival': '13:00', 'duration': '6h 00m',
                'price': 350, 'total_seats': 40, 'rating': 4.0,
                'amenities': ['WiFi'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Chandipur Beach'],
                'reviews': [],
            },
            {
                'bus_id': 'bus038', 'name': 'Similipal Rider', 'operator': 'Private',
                'bus_type': 'Sleeper', 'from_city': 'Bhubaneswar', 'to_city': 'Similipal',
                'departure': '21:00', 'arrival': '05:30', 'duration': '8h 30m',
                'price': 600, 'total_seats': 30, 'rating': 4.2,
                'amenities': ['Blanket'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Similipal Gate'],
                'reviews': [],
            },
            {
                'bus_id': 'bus039', 'name': 'Talcher Express', 'operator': 'OSRTC',
                'bus_type': 'Non-AC', 'from_city': 'Cuttack', 'to_city': 'Talcher',
                'departure': '09:00', 'arrival': '13:00', 'duration': '4h 00m',
                'price': 220, 'total_seats': 45, 'rating': 3.8,
                'amenities': ['Charging Point'],
                'boarding_points': ['Cuttack Bus Stand'],
                'dropping_points': ['Talcher Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus040', 'name': 'Hirakud Express', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Hirakud',
                'departure': '06:00', 'arrival': '13:30', 'duration': '7h 30m',
                'price': 480, 'total_seats': 40, 'rating': 4.1,
                'amenities': ['WiFi'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Hirakud Dam'],
                'reviews': [],
            },

            # ================= COMPLETE ODISHA UP TO bus066 =================
            {
                'bus_id': 'bus041', 'name': 'Kendujhar Deluxe', 'operator': 'Private',
                'bus_type': 'AC', 'from_city': 'Bhubaneswar', 'to_city': 'Keonjhar',
                'departure': '08:00', 'arrival': '14:30', 'duration': '6h 30m',
                'price': 420, 'total_seats': 40, 'rating': 4.0,
                'amenities': ['WiFi'],
                'boarding_points': ['Bhubaneswar ISBT'],
                'dropping_points': ['Keonjhar Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus042', 'name': 'Sundargarh Express', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Rourkela', 'to_city': 'Sundargarh',
                'departure': '07:30', 'arrival': '10:30', 'duration': '3h 00m',
                'price': 200, 'total_seats': 40, 'rating': 4.0,
                'amenities': ['Charging Point'],
                'boarding_points': ['Rourkela Bus Stand'],
                'dropping_points': ['Sundargarh Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus043', 'name': 'Bargarh Rider', 'operator': 'Private',
                'bus_type': 'Non-AC', 'from_city': 'Sambalpur', 'to_city': 'Bargarh',
                'departure': '09:00', 'arrival': '11:00', 'duration': '2h 00m',
                'price': 120, 'total_seats': 45, 'rating': 3.9,
                'amenities': ['Charging Point'],
                'boarding_points': ['Sambalpur Bus Stand'],
                'dropping_points': ['Bargarh Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus044', 'name': 'Puri Coastal Express', 'operator': 'OSRTC',
                'bus_type': 'AC', 'from_city': 'Cuttack', 'to_city': 'Puri',
                'departure': '07:00', 'arrival': '10:00', 'duration': '3h 00m',
                'price': 180, 'total_seats': 40, 'rating': 4.3,
                'amenities': ['WiFi'],
                'boarding_points': ['Cuttack Bus Stand'],
                'dropping_points': ['Puri Beach Road'],
                'reviews': [],
            },

            # ================= INDIA ROUTES (bus067–bus096) =================
            {
                'bus_id': 'bus067', 'name': 'Delhi Jaipur Express', 'operator': 'Private',
                'bus_type': 'AC', 'from_city': 'Delhi', 'to_city': 'Jaipur',
                'departure': '08:00', 'arrival': '14:00', 'duration': '6h 00m',
                'price': 700, 'total_seats': 40, 'rating': 4.2,
                'amenities': ['WiFi', 'Charging Point'],
                'boarding_points': ['Delhi ISBT'],
                'dropping_points': ['Jaipur Bus Stand'],
                'reviews': [],
            },
            {
                'bus_id': 'bus068', 'name': 'Mumbai Pune Express', 'operator': 'Private',
                'bus_type': 'AC', 'from_city': 'Mumbai', 'to_city': 'Pune',
                'departure': '09:00', 'arrival': '13:00', 'duration': '4h 00m',
                'price': 500, 'total_seats': 40, 'rating': 4.3,
                'amenities': ['WiFi'],
                'boarding_points': ['Mumbai Central'],
                'dropping_points': ['Pune Station'],
                'reviews': [],
            },
            {
                'bus_id': 'bus069', 'name': 'Bangalore Goa Sleeper', 'operator': 'Private',
                'bus_type': 'Sleeper', 'from_city': 'Bangalore', 'to_city': 'Goa',
                'departure': '20:00', 'arrival': '07:00', 'duration': '11h 00m',
                'price': 1200, 'total_seats': 30, 'rating': 4.4,
                'amenities': ['Blanket', 'Charging Point'],
                'boarding_points': ['Majestic Bus Stand'],
                'dropping_points': ['Panaji'],
                'reviews': [],
            },
            {
                'bus_id': 'bus070', 'name': 'Hyderabad Chennai Express', 'operator': 'Private',
                'bus_type': 'AC', 'from_city': 'Hyderabad', 'to_city': 'Chennai',
                'departure': '21:00', 'arrival': '06:00', 'duration': '9h 00m',
                'price': 900, 'total_seats': 40, 'rating': 4.1,
                'amenities': ['WiFi'],
                'boarding_points': ['Hyderabad MGBS'],
                'dropping_points': ['Chennai Koyambedu'],
                'reviews': [],
            },
            {
                'bus_id': 'bus071', 'name': 'Delhi Chandigarh Express', 'operator': 'Private',
                'bus_type': 'AC', 'from_city': 'Delhi', 'to_city': 'Chandigarh',
                'departure': '07:00', 'arrival': '11:30', 'duration': '4h 30m',
                'price': 600, 'total_seats': 40, 'rating': 4.2,
                'amenities': ['WiFi'],
                'boarding_points': ['Delhi ISBT'],
                'dropping_points': ['Chandigarh Bus Stand'],
                'reviews': [],
            },
]
        for bd in buses_data:
            reviews = bd.pop('reviews')
            amenities = bd.pop('amenities')
            boarding = bd.pop('boarding_points')
            dropping = bd.pop('dropping_points')
            bus = Bus(**bd)
            bus.set_amenities(amenities)
            bus.set_boarding_points(boarding)
            bus.set_dropping_points(dropping)
            bus.save()
            for r in reviews:
                BusReview.objects.create(bus=bus, **r)

    if not AdminUser.objects.exists():
        AdminUser.objects.create(email='admin@busbook.com', password='admin123', name='Admin')


# ─── Public Pages ─────────────────────────────────────────────────────────────

def index(request):
    seed_data()
    user = get_session_user(request)
    return render(request, 'booking/index.html', {'user': user})


def search(request):
    seed_data()
    user = get_session_user(request)
    from_city = request.GET.get('from', '')
    to_city = request.GET.get('to', '')
    travel_date = request.GET.get('date', date.today().isoformat())

    buses = []
    if from_city and to_city:
        qs = Bus.objects.filter(
            from_city__iexact=from_city,
            to_city__iexact=to_city
        )
        for bus in qs:
            booked = bus.get_booked_seats()
            buses.append({
                'id': bus.bus_id,
                'name': bus.name,
                'operator': bus.operator,
                'type': bus.bus_type,
                'from': bus.from_city,
                'to': bus.to_city,
                'departure': bus.departure,
                'arrival': bus.arrival,
                'duration': bus.duration,
                'price': bus.price,
                'totalSeats': bus.total_seats,
                'bookedSeats': booked,
                'seatsLeft': bus.total_seats - len(booked),
                'amenities': bus.get_amenities(),
                'rating': bus.rating,
            })

    return render(request, 'booking/search.html', {
        'user': user,
        'buses_json': json.dumps(buses),
        'from_city': from_city,
        'to_city': to_city,
        'travel_date': travel_date,
    })


def bus_detail(request):
    seed_data()
    user = get_session_user(request)
    bus_id = request.GET.get('busId', '')
    travel_date = request.GET.get('date', date.today().isoformat())
    from_city = request.GET.get('from', '')
    to_city = request.GET.get('to', '')

    try:
        bus_obj = Bus.objects.get(bus_id=bus_id)
    except Bus.DoesNotExist:
        return render(request, 'booking/bus_detail.html', {'bus': None, 'user': user})

    booked_seats = bus_obj.get_booked_seats()
    reviews = [{'user': r.user_name, 'comment': r.comment, 'stars': r.stars}
               for r in bus_obj.reviews.all()]

    bus_data = {
        'id': bus_obj.bus_id,
        'name': bus_obj.name,
        'operator': bus_obj.operator,
        'type': bus_obj.bus_type,
        'from': bus_obj.from_city,
        'to': bus_obj.to_city,
        'departure': bus_obj.departure,
        'arrival': bus_obj.arrival,
        'duration': bus_obj.duration,
        'price': bus_obj.price,
        'totalSeats': bus_obj.total_seats,
        'bookedSeats': booked_seats,
        'amenities': bus_obj.get_amenities(),
        'boardingPoints': bus_obj.get_boarding_points(),
        'droppingPoints': bus_obj.get_dropping_points(),
        'rating': bus_obj.rating,
        'reviews': reviews,
    }

    return render(request, 'booking/bus_detail.html', {
        'user': user,
        'bus_json': json.dumps(bus_data),
        'travel_date': travel_date,
        'from_city': from_city,
        'to_city': to_city,
    })


def checkout(request):
    user = get_session_user(request)
    if not user:
        return redirect('/login/?redirect=/checkout/')

    temp_booking = request.session.get('temp_booking')
    if not temp_booking:
        return redirect('/')

    return render(request, 'booking/checkout.html', {
        'user': user,
        'temp_booking_json': json.dumps(temp_booking),
    })


def ticket_view(request):
    user = get_session_user(request)
    booking_id = request.GET.get('id', request.session.get('last_booking_id', ''))
    autoprint = request.GET.get('autoprint', '0')

    try:
        booking = Booking.objects.get(booking_id=booking_id)
        passengers = list(booking.passengers.values('name', 'age', 'gender', 'seat'))
        booking_data = {
            'bookingId': booking.booking_id,
            'busName': booking.bus_name,
            'type': booking.bus_type,
            'from': booking.from_city,
            'to': booking.to_city,
            'departure': booking.departure,
            'arrival': booking.arrival,
            'duration': booking.duration,
            'travelDate': booking.travel_date.isoformat(),
            'seats': booking.get_seats(),
            'totalFare': booking.total_fare,
            'boardingPoint': booking.boarding_point,
            'droppingPoint': booking.dropping_point,
            'contactEmail': booking.contact_email,
            'contactPhone': booking.contact_phone,
            'paymentMethod': booking.payment_method,
            'status': booking.status,
            'passengers': passengers,
        }
    except Booking.DoesNotExist:
        booking_data = None

    return render(request, 'booking/ticket.html', {
        'user': user,
        'booking_json': json.dumps(booking_data),
        'autoprint': autoprint,
    })


def my_bookings(request):
    user = get_session_user(request)
    if not user:
        return redirect('/login/?redirect=/bookings/')
    return render(request, 'booking/bookings.html', {'user': user})


def profile(request):
    user = get_session_user(request)
    if not user:
        return redirect('/login/?redirect=/profile/')
    bookings = Booking.objects.filter(user=user)
    confirmed_count = bookings.filter(status='Confirmed').count()
    cancelled_count = bookings.filter(status='Cancelled').count()
    total_spent = sum(b.total_fare for b in bookings.filter(status='Confirmed'))
    return render(request, 'booking/profile.html', {
        'user': user,
        'confirmed_count': confirmed_count,
        'cancelled_count': cancelled_count,
        'total_spent': total_spent,
    })


def login_view(request):
    user = get_session_user(request)
    if user:
        return redirect('/')
    return render(request, 'booking/login.html', {'redirect': request.GET.get('redirect', '')})


def register_view(request):
    user = get_session_user(request)
    if user:
        return redirect('/')
    return render(request, 'booking/register.html')


def admin_login_view(request):
    if is_admin_session(request):
        return redirect('/admin-panel/')
    return render(request, 'booking/admin_login.html')


def admin_panel(request):
    if not is_admin_session(request):
        return redirect('/admin-login/')
    return render(request, 'booking/admin.html')


# ─── API Endpoints (JSON) ─────────────────────────────────────────────────────

@require_POST
def api_login(request):
    data = json.loads(request.body)
    email = data.get('email', '').strip()
    password = data.get('password', '')
    try:
        user = User.objects.get(email=email)
        if user.password == password:
            request.session['user_id'] = user.id
            return JsonResponse({'success': True, 'name': user.name})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid email or password'})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid email or password'})


@require_POST
def api_register(request):
    data = json.loads(request.body)
    email = data.get('email', '').strip()
    if User.objects.filter(email=email).exists():
        return JsonResponse({'success': False, 'error': 'Account with this email already exists'})
    user = User.objects.create(
        name=data.get('name', ''),
        email=email,
        phone=data.get('phone', ''),
        age=data.get('age') or None,
        gender=data.get('gender', ''),
        password=data.get('password', ''),
    )
    request.session['user_id'] = user.id
    return JsonResponse({'success': True, 'name': user.name})


@require_GET
def api_logout(request):
    request.session.pop('user_id', None)
    return JsonResponse({'success': True})


@require_POST
def api_admin_login(request):
    data = json.loads(request.body)
    email = data.get('email', '').strip()
    password = data.get('password', '')
    try:
        admin = AdminUser.objects.get(email=email)
        if admin.password == password:
            request.session['admin_logged_in'] = True
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'error': 'Invalid admin credentials'})
    except AdminUser.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Invalid admin credentials'})


@require_GET
def api_admin_logout(request):
    request.session.pop('admin_logged_in', None)
    return JsonResponse({'success': True})


@require_POST
def api_save_temp_booking(request):
    data = json.loads(request.body)
    request.session['temp_booking'] = data
    return JsonResponse({'success': True})


@require_POST
def api_confirm_booking(request):
    user = get_session_user(request)
    if not user:
        return JsonResponse({'success': False, 'error': 'Not logged in'})

    data = json.loads(request.body)
    temp = data.get('temp_booking', {})
    passengers_data = data.get('passengers', [])

    try:
        bus = Bus.objects.get(bus_id=temp['busId'])
    except Bus.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Bus not found'})

    booking_id = generate_booking_id()
    seats = temp.get('seats', [])

    booking = Booking.objects.create(
        booking_id=booking_id,
        bus=bus,
        user=user,
        bus_name=temp['busName'],
        bus_type=temp['type'],
        from_city=temp['from'],
        to_city=temp['to'],
        departure=temp['departure'],
        arrival=temp['arrival'],
        duration=temp['duration'],
        travel_date=date.fromisoformat(temp['travelDate']),
        seats=json.dumps(seats),
        price_per_seat=temp['pricePerSeat'],
        base_fare=temp['baseFare'],
        tax=temp['tax'],
        convenience=temp['convenience'],
        total_fare=temp['totalFare'],
        boarding_point=data.get('boardingPoint', ''),
        dropping_point=data.get('droppingPoint', ''),
        contact_email=data.get('contactEmail', user.email),
        contact_phone=data.get('contactPhone', ''),
        payment_method=data.get('paymentMethod', 'upi'),
        status='Confirmed',
    )

    for p in passengers_data:
        Passenger.objects.create(
            booking=booking,
            name=p['name'],
            age=p['age'],
            gender=p['gender'],
            seat=p['seat'],
        )

    request.session.pop('temp_booking', None)
    request.session['last_booking_id'] = booking_id

    return JsonResponse({'success': True, 'bookingId': booking_id})


@require_GET
def api_my_bookings(request):
    user = get_session_user(request)
    if not user:
        return JsonResponse({'success': False, 'error': 'Not logged in'})

    bookings = Booking.objects.filter(user=user).order_by('-booked_at')
    result = []
    for b in bookings:
        passengers = list(b.passengers.values('name', 'age', 'gender', 'seat'))
        result.append({
            'bookingId': b.booking_id,
            'busId': b.bus.bus_id,
            'busName': b.bus_name,
            'type': b.bus_type,
            'from': b.from_city,
            'to': b.to_city,
            'departure': b.departure,
            'arrival': b.arrival,
            'duration': b.duration,
            'travelDate': b.travel_date.isoformat(),
            'seats': b.get_seats(),
            'totalFare': b.total_fare,
            'paymentMethod': b.payment_method,
            'status': b.status,
            'refundStatus': b.refund_status,
            'refundAmount': b.refund_amount,
            'reviewed': b.reviewed,
            'passengers': passengers,
        })
    return JsonResponse({'success': True, 'bookings': result})


@require_POST
def api_cancel_booking(request):
    user = get_session_user(request)
    if not user:
        return JsonResponse({'success': False, 'error': 'Not logged in'})

    data = json.loads(request.body)
    booking_id = data.get('bookingId')

    try:
        booking = Booking.objects.get(booking_id=booking_id, user=user)
    except Booking.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Booking not found'})

    if booking.status == 'Cancelled':
        return JsonResponse({'success': False, 'error': 'Already cancelled'})

    now = datetime.now()
    travel_dt = datetime.combine(booking.travel_date, datetime.strptime(booking.departure, '%H:%M').time())
    hours_left = (travel_dt - now).total_seconds() / 3600

    if hours_left >= 24:
        refund_amt = booking.total_fare
        refund_status = 'Full Refund'
    elif hours_left > 0:
        refund_amt = int(booking.total_fare * 0.5)
        refund_status = 'Partial Refund (50%)'
    else:
        refund_amt = 0
        refund_status = 'No Refund'

    booking.status = 'Cancelled'
    booking.refund_amount = refund_amt
    booking.refund_status = refund_status
    booking.save()

    return JsonResponse({
        'success': True,
        'refundStatus': refund_status,
        'refundAmount': refund_amt,
    })


@require_POST
def api_submit_review(request):
    user = get_session_user(request)
    if not user:
        return JsonResponse({'success': False, 'error': 'Not logged in'})

    data = json.loads(request.body)
    bus_id = data.get('busId')
    booking_id = data.get('bookingId')
    stars = data.get('stars')
    comment = data.get('comment', '').strip()

    try:
        bus = Bus.objects.get(bus_id=bus_id)
        booking = Booking.objects.get(booking_id=booking_id, user=user)
    except (Bus.DoesNotExist, Booking.DoesNotExist):
        return JsonResponse({'success': False, 'error': 'Not found'})

    BusReview.objects.create(bus=bus, user_name=user.name, comment=comment, stars=stars)
    bus.recalculate_rating()
    booking.reviewed = True
    booking.save()

    return JsonResponse({'success': True})


@require_POST
def api_update_profile(request):
    user = get_session_user(request)
    if not user:
        return JsonResponse({'success': False, 'error': 'Not logged in'})

    data = json.loads(request.body)
    user.name = data.get('name', user.name)
    user.age = data.get('age') or user.age
    user.phone = data.get('phone', user.phone)
    user.gender = data.get('gender', user.gender)
    user.save()
    return JsonResponse({'success': True, 'name': user.name})


@require_POST
def api_change_password(request):
    user = get_session_user(request)
    if not user:
        return JsonResponse({'success': False, 'error': 'Not logged in'})

    data = json.loads(request.body)
    cur = data.get('current', '')
    new = data.get('new', '')

    if cur != user.password:
        return JsonResponse({'success': False, 'error': 'Current password is wrong'})

    user.password = new
    user.save()
    return JsonResponse({'success': True})


@require_POST
def api_reset_password(request):
    data = json.loads(request.body)
    email = data.get('email', '').strip()
    new_password = data.get('newPassword', '')
    try:
        user = User.objects.get(email=email)
        user.password = new_password
        user.save()
        return JsonResponse({'success': True})
    except User.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No account found with this email'})


@require_GET
def api_check_email(request):
    email = request.GET.get('email', '').strip()
    exists = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': exists})


# ─── Admin API ────────────────────────────────────────────────────────────────

@require_GET
def api_admin_stats(request):
    if not is_admin_session(request):
        return JsonResponse({'success': False, 'error': 'Not admin'})

    bookings = Booking.objects.all()
    confirmed = bookings.filter(status='Confirmed')
    revenue = sum(b.total_fare for b in confirmed)

    return JsonResponse({
        'success': True,
        'totalBookings': bookings.count(),
        'revenue': revenue,
        'totalBuses': Bus.objects.count(),
        'totalUsers': User.objects.count(),
        'cancelledCount': bookings.filter(status='Cancelled').count(),
    })


@require_GET
def api_admin_buses(request):
    if not is_admin_session(request):
        return JsonResponse({'success': False, 'error': 'Not admin'})
    buses = []
    for b in Bus.objects.all():
        booked = b.get_booked_seats()
        buses.append({
            'id': b.bus_id,
            'name': b.name,
            'operator': b.operator,
            'type': b.bus_type,
            'from': b.from_city,
            'to': b.to_city,
            'departure': b.departure,
            'arrival': b.arrival,
            'duration': b.duration,
            'price': b.price,
            'totalSeats': b.total_seats,
            'seatsLeft': b.total_seats - len(booked),
            'amenities': b.get_amenities(),
            'boardingPoints': b.get_boarding_points(),
            'droppingPoints': b.get_dropping_points(),
            'rating': b.rating,
        })
    return JsonResponse({'success': True, 'buses': buses})


@require_POST
def api_admin_save_bus(request):
    if not is_admin_session(request):
        return JsonResponse({'success': False, 'error': 'Not admin'})

    data = json.loads(request.body)
    bus_id = data.get('id')

    if bus_id:
        try:
            bus = Bus.objects.get(bus_id=bus_id)
        except Bus.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Bus not found'})
        action = 'updated'
    else:
        import time as _time
        bus = Bus(bus_id='bus' + str(int(_time.time() * 1000)))
        action = 'added'

    bus.name = data.get('name', '')
    bus.operator = data.get('operator', '')
    bus.bus_type = data.get('type', 'AC')
    bus.from_city = data.get('from', '')
    bus.to_city = data.get('to', '')
    bus.departure = data.get('departure', '')
    bus.arrival = data.get('arrival', '')
    bus.duration = data.get('duration', '')
    bus.price = int(data.get('price', 0))
    bus.total_seats = int(data.get('totalSeats', 40))
    bus.set_amenities(data.get('amenities', []))
    bus.set_boarding_points(data.get('boardingPoints', []))
    bus.set_dropping_points(data.get('droppingPoints', []))
    bus.save()

    return JsonResponse({'success': True, 'action': action})


@require_POST
def api_admin_delete_bus(request):
    if not is_admin_session(request):
        return JsonResponse({'success': False, 'error': 'Not admin'})
    data = json.loads(request.body)
    Bus.objects.filter(bus_id=data.get('id')).delete()
    return JsonResponse({'success': True})


@require_GET
def api_admin_all_bookings(request):
    if not is_admin_session(request):
        return JsonResponse({'success': False, 'error': 'Not admin'})
    bookings = Booking.objects.select_related('user').order_by('-booked_at')
    result = []
    for b in bookings:
        result.append({
            'bookingId': b.booking_id,
            'userName': b.user.name,
            'userEmail': b.user.email,
            'from': b.from_city,
            'to': b.to_city,
            'seats': b.get_seats(),
            'travelDate': b.travel_date.isoformat(),
            'totalFare': b.total_fare,
            'status': b.status,
            'type': b.bus_type,
        })
    return JsonResponse({'success': True, 'bookings': result})


@require_GET
def api_admin_users(request):
    if not is_admin_session(request):
        return JsonResponse({'success': False, 'error': 'Not admin'})
    users = User.objects.all().order_by('created_at')
    result = []
    for u in users:
        bks = Booking.objects.filter(user=u)
        spent = sum(b.total_fare for b in bks.filter(status='Confirmed'))
        result.append({
            'name': u.name,
            'email': u.email,
            'phone': u.phone,
            'gender': u.gender,
            'age': u.age,
            'createdAt': u.created_at.strftime('%d/%m/%Y'),
            'bookingCount': bks.count(),
            'totalSpent': spent,
        })
    return JsonResponse({'success': True, 'users': result})


@require_GET
def api_admin_booking_charts(request):
    if not is_admin_session(request):
        return JsonResponse({'success': False, 'error': 'Not admin'})
    bookings = Booking.objects.all()
    type_counts = {}
    revenue_by_type = {}
    for b in bookings:
        type_counts[b.bus_type] = type_counts.get(b.bus_type, 0) + 1
        if b.status == 'Confirmed':
            revenue_by_type[b.bus_type] = revenue_by_type.get(b.bus_type, 0) + b.total_fare
    return JsonResponse({
        'success': True,
        'typeCounts': type_counts,
        'revenueByType': revenue_by_type,
    })
