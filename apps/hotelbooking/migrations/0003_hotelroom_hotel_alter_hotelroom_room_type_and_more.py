# Generated by Django 5.1.6 on 2025-04-07 13:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelbooking', '0002_hotelrevenue_hotelroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotelroom',
            name='hotel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='hotelbooking.hotelbooking'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hotelroom',
            name='room_type',
            field=models.CharField(choices=[('Deluxe', 'Deluxe'), ('Suite', 'Suite'), ('Standard', 'Standard')], max_length=100),
        ),
        migrations.CreateModel(
            name='HotelAmenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amenity', models.CharField(max_length=100)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amenities', to='hotelbooking.hotelbooking')),
            ],
        ),
        migrations.CreateModel(
            name='RoomAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('available_date', models.DateField()),
                ('is_available', models.BooleanField(default=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='hotelbooking.hotelroom')),
            ],
        ),
    ]
