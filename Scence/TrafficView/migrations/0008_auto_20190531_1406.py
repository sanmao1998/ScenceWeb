# Generated by Django 2.2.1 on 2019-05-31 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TrafficView', '0007_auto_20190531_1255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yearcitytraffic',
            old_name='index',
            new_name='TrafficIndex',
        ),
    ]
