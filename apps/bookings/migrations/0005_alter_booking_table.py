# Generated by Django 5.1.6 on 2025-04-07 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_booking_latitude_booking_location_booking_longitude_and_more'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='booking',
            table='bookings',
        ),
    ]
