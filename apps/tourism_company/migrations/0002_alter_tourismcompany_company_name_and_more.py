# Generated by Django 5.1.6 on 2025-03-16 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourism_company', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tourismcompany',
            name='company_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='tourismcompany',
            name='user_email',
            field=models.EmailField(max_length=55, unique=True),
        ),
    ]
