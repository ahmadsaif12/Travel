# Generated by Django 5.1.6 on 2025-04-07 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tour_package', '0005_tourismcompany_remove_tourpackage_company_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tourpackage',
            old_name='company',
            new_name='tourism_company',
        ),
        migrations.AlterModelTable(
            name='tourpackage',
            table='tour_package',
        ),
    ]
