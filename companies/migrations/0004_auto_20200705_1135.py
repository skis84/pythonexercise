# Generated by Django 3.0.8 on 2020-07-05 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20200705_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='modified_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='modified_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='website',
            name='modified_date',
            field=models.DateTimeField(),
        ),
    ]
