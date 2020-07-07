# Generated by Django 3.0.8 on 2020-07-06 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0007_auto_20200706_0902'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='modified_date',
            new_name='modified',
        ),
        migrations.RenameField(
            model_name='name',
            old_name='modified_date',
            new_name='modified',
        ),
        migrations.RenameField(
            model_name='phonenumber',
            old_name='modified_date',
            new_name='modified',
        ),
        migrations.RenameField(
            model_name='website',
            old_name='modified_date',
            new_name='modified',
        ),
        migrations.AlterField(
            model_name='address',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='registration_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='name',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='name',
            name='registration_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='phonenumber',
            name='registration_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='website',
            name='end_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='website',
            name='registration_date',
            field=models.DateField(),
        ),
    ]