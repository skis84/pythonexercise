# Generated by Django 3.0.8 on 2020-07-06 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_auto_20200705_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='website',
            name='modified_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
