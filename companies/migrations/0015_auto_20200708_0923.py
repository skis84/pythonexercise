# Generated by Django 3.0.8 on 2020-07-08 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0014_remove_address_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='name',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='website',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]