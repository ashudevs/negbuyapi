# Generated by Django 3.2.6 on 2024-01-05 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('negbuyapi', '0002_auto_20240105_1203'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topclients',
            old_name='location',
            new_name='order_location',
        ),
        migrations.RenameField(
            model_name='topclients',
            old_name='quantity',
            new_name='order_quantity',
        ),
        migrations.RemoveField(
            model_name='topclients',
            name='product',
        ),
        migrations.AddField(
            model_name='topclients',
            name='client_status',
            field=models.BooleanField(default=False),
        ),
    ]
