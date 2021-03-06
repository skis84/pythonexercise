# Generated by Django 3.0.8 on 2020-07-08 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0019_company_business_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='registration_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='name',
            name='registration_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='registration_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='website',
            name='registration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
