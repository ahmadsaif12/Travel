# Generated by Django 5.1.6 on 2025-04-07 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_login', '0008_auto_20250402_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
