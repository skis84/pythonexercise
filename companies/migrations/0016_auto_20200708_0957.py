# Generated by Django 3.0.8 on 2020-07-08 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0015_auto_20200708_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='language',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='name',
            name='language',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='language',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='website',
            name='language',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
