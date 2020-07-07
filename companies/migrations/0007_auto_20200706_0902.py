# Generated by Django 3.0.8 on 2020-07-06 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_auto_20200706_0534'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='name',
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(max_length=255)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.Company')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]