from django.db import models
import json


class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=200)  # plain text for demo (B.Tech project)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Bus(models.Model):
    bus_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    operator = models.CharField(max_length=100)
    bus_type = models.CharField(max_length=20, choices=[
        ('AC', 'AC'), ('Non-AC', 'Non-AC'), ('Sleeper', 'Sleeper')
    ])
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    departure = models.CharField(max_length=10)  # e.g. "06:00"
    arrival = models.CharField(max_length=10)
    duration = models.CharField(max_length=20)
    price = models.IntegerField()
    total_seats = models.IntegerField(default=40)
    amenities = models.TextField(default='[]')        # JSON list
    boarding_points = models.TextField(default='[]')  # JSON list
    dropping_points = models.TextField(default='[]')  # JSON list
    rating = models.FloatField(default=4.0)

    def get_amenities(self):
        return json.loads(self.amenities)

    def get_boarding_points(self):
        return json.loads(self.boarding_points)

    def get_dropping_points(self):
        return json.loads(self.dropping_points)

    def set_amenities(self, lst):
        self.amenities = json.dumps(lst)

    def set_boarding_points(self, lst):
        self.boarding_points = json.dumps(lst)

    def set_dropping_points(self, lst):
        self.dropping_points = json.dumps(lst)

    def booked_seats_list(self):
        return list(self.bookings.filter(status='Confirmed').values_list('seats', flat=True))

    def get_booked_seats(self):
        seats = []
        for b in self.bookings.filter(status='Confirmed'):
            seats.extend(json.loads(b.seats))
        return seats

    def available_seats(self):
        return self.total_seats - len(self.get_booked_seats())

    def get_reviews(self):
        return list(self.reviews.values('user_name', 'comment', 'stars'))

    def recalculate_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            self.rating = round(sum(r.stars for r in reviews) / reviews.count(), 1)
            self.save()

    def __str__(self):
        return f"{self.name} ({self.from_city} → {self.to_city})"


class BusReview(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=200)
    comment = models.TextField()
    stars = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.bus.name} ({self.stars}★)"


class Booking(models.Model):
    STATUS_CHOICES = [('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')]

    booking_id = models.CharField(max_length=50, unique=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    bus_name = models.CharField(max_length=200)
    bus_type = models.CharField(max_length=20)
    from_city = models.CharField(max_length=100)
    to_city = models.CharField(max_length=100)
    departure = models.CharField(max_length=10)
    arrival = models.CharField(max_length=10)
    duration = models.CharField(max_length=20)
    travel_date = models.DateField()
    seats = models.TextField()          # JSON list of seat IDs
    price_per_seat = models.IntegerField()
    base_fare = models.IntegerField()
    tax = models.IntegerField()
    convenience = models.IntegerField(default=30)
    total_fare = models.IntegerField()
    boarding_point = models.CharField(max_length=200)
    dropping_point = models.CharField(max_length=200)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    payment_method = models.CharField(max_length=30)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Confirmed')
    refund_status = models.CharField(max_length=50, blank=True)
    refund_amount = models.IntegerField(default=0)
    reviewed = models.BooleanField(default=False)
    booked_at = models.DateTimeField(auto_now_add=True)

    def get_seats(self):
        return json.loads(self.seats)

    def set_seats(self, lst):
        self.seats = json.dumps(lst)

    def __str__(self):
        return f"{self.booking_id} - {self.user.name}"


class Passenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    seat = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} ({self.seat})"


class AdminUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=100, default='Admin')

    def __str__(self):
        return self.email
