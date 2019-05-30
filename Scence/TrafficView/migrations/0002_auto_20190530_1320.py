# Generated by Django 2.2.1 on 2019-05-30 13:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TrafficView', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maincitytrafficdatabase',
            name='cityCode',
            field=models.IntegerField(unique=True, verbose_name='城市ip'),
        ),
        migrations.CreateModel(
            name='YearCityTraffic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('city', models.CharField(max_length=32)),
                ('index', models.FloatField()),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='YearTraffic', to='TrafficView.MainCityTrafficDataBase', to_field='cityCode', verbose_name='城市季度交通ip')),
            ],
            options={
                'db_table': 'YearCityTraffic',
            },
        ),
        migrations.CreateModel(
            name='RoadTraffic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('DetailTime', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('direction', models.TextField()),
                ('speed', models.FloatField()),
                ('data', models.TextField()),
                ('bounds', models.TextField()),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='RoadTraffic', to='TrafficView.MainCityTrafficDataBase', to_field='cityCode', verbose_name='城市道路交通ip')),
            ],
            options={
                'db_table': 'RoadTraffic',
                'ordering': ['speed'],
            },
        ),
        migrations.CreateModel(
            name='CityTraffic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(max_length=32)),
                ('data', models.FloatField()),
                ('time', models.CharField(max_length=16)),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CityTraffic', to='TrafficView.MainCityTrafficDataBase', to_field='cityCode', verbose_name='城市交通ip')),
            ],
            options={
                'db_table': 'CityTraffic',
                'ordering': ['time'],
            },
        ),
    ]