from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=200)),
                ('name', models.CharField(default='Admin', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_id', models.CharField(max_length=50, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('operator', models.CharField(max_length=100)),
                ('bus_type', models.CharField(choices=[('AC', 'AC'), ('Non-AC', 'Non-AC'), ('Sleeper', 'Sleeper')], max_length=20)),
                ('from_city', models.CharField(max_length=100)),
                ('to_city', models.CharField(max_length=100)),
                ('departure', models.CharField(max_length=10)),
                ('arrival', models.CharField(max_length=10)),
                ('duration', models.CharField(max_length=20)),
                ('price', models.IntegerField()),
                ('total_seats', models.IntegerField(default=40)),
                ('amenities', models.TextField(default='[]')),
                ('boarding_points', models.TextField(default='[]')),
                ('dropping_points', models.TextField(default='[]')),
                ('rating', models.FloatField(default=4.0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=30)),
                ('password', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BusReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200)),
                ('comment', models.TextField()),
                ('stars', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='booking.bus')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(max_length=50, unique=True)),
                ('bus_name', models.CharField(max_length=200)),
                ('bus_type', models.CharField(max_length=20)),
                ('from_city', models.CharField(max_length=100)),
                ('to_city', models.CharField(max_length=100)),
                ('departure', models.CharField(max_length=10)),
                ('arrival', models.CharField(max_length=10)),
                ('duration', models.CharField(max_length=20)),
                ('travel_date', models.DateField()),
                ('seats', models.TextField()),
                ('price_per_seat', models.IntegerField()),
                ('base_fare', models.IntegerField()),
                ('tax', models.IntegerField()),
                ('convenience', models.IntegerField(default=30)),
                ('total_fare', models.IntegerField()),
                ('boarding_point', models.CharField(max_length=200)),
                ('dropping_point', models.CharField(max_length=200)),
                ('contact_email', models.EmailField(max_length=254)),
                ('contact_phone', models.CharField(max_length=15)),
                ('payment_method', models.CharField(max_length=30)),
                ('status', models.CharField(choices=[('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Confirmed', max_length=20)),
                ('refund_status', models.CharField(blank=True, max_length=50)),
                ('refund_amount', models.IntegerField(default=0)),
                ('reviewed', models.BooleanField(default=False)),
                ('booked_at', models.DateTimeField(auto_now_add=True)),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='booking.bus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='booking.user')),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=20)),
                ('seat', models.CharField(max_length=10)),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='passengers', to='booking.booking')),
            ],
        ),
    ]
