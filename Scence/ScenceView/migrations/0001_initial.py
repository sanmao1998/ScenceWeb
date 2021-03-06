# Generated by Django 2.2.1 on 2019-05-12 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JingQuDatabase',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=32, verbose_name='景区名字')),
                ('bounds_lon', models.FloatField(verbose_name='经纬度')),
                ('bounds_lat', models.FloatField(verbose_name='经纬度')),
                ('PeoplePid', models.IntegerField(verbose_name='景区ip')),
                ('CityCode', models.IntegerField(default=0, verbose_name='城市交通ip')),
                ('WeatherPid', models.CharField(max_length=32, verbose_name='天气情况ip')),
                ('PeopleTablePid', models.IntegerField(unique=True, verbose_name='景区表')),
                ('CityTableCode', models.IntegerField(unique=True, verbose_name='城市交通表')),
                ('WeatherTablePid', models.IntegerField(max_length=32, unique=True, verbose_name='天气情况表')),
            ],
            options={
                'db_table': 'ScenceInfoData',
            },
        ),
    ]
