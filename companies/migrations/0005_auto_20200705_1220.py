# Generated by Django 3.0.8 on 2020-07-05 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_auto_20200705_1135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='phonenumber',
            old_name='phone_number',
            new_name='value',
        ),
        migrations.RenameField(
            model_name='website',
            old_name='url',
            new_name='value',
        ),
    ]
