# Generated by Django 3.0.8 on 2020-07-08 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0017_auto_20200708_1003'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='address',
            options={'ordering': ('-modified',)},
        ),
        migrations.AlterModelOptions(
            name='name',
            options={'ordering': ('-modified',)},
        ),
        migrations.AlterModelOptions(
            name='phonenumber',
            options={'ordering': ('-modified',)},
        ),
        migrations.AlterModelOptions(
            name='website',
            options={'ordering': ('-modified',)},
        ),
    ]