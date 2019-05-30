# Generated by Django 2.2.1 on 2019-05-12 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('WebView', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(max_length=32, verbose_name='日期')),
                ('detailTime', models.CharField(max_length=16, verbose_name='时间点')),
                ('state', models.CharField(max_length=32, verbose_name='天气状态')),
                ('temperature', models.IntegerField(verbose_name='气温')),
                ('wind', models.CharField(max_length=32, verbose_name='风力风向')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weather', to='WebView.JingQuDatabase', to_field='WeatherTablePid', verbose_name='景区pid')),
            ],
            options={
                'db_table': 'weather',
                'ordering': ['detailTime'],
            },
        ),
        migrations.CreateModel(
            name='Traffic_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(max_length=32, verbose_name='日期')),
                ('index', models.FloatField(verbose_name='交通拥堵指数')),
                ('detailTime', models.CharField(max_length=16, verbose_name='时间点')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='traffic', to='WebView.JingQuDatabase', to_field='CityTableCode', verbose_name='景区pid')),
            ],
            options={
                'db_table': 'traffic',
                'ordering': ['detailTime'],
            },
        ),
        migrations.CreateModel(
            name='PeopleFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=32, verbose_name='日期')),
                ('num', models.IntegerField(verbose_name='客流')),
                ('detailTime', models.CharField(max_length=16, verbose_name='时间点')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Flow', to='WebView.JingQuDatabase', to_field='PeopleTablePid', verbose_name='景区pid')),
            ],
            options={
                'db_table': 'peopleFlow',
                'ordering': ['detailTime'],
            },
        ),
        migrations.AddIndex(
            model_name='weather_data',
            index=models.Index(fields=['pid'], name='景区pid'),
        ),
        migrations.AddIndex(
            model_name='weather_data',
            index=models.Index(fields=['date'], name='Day'),
        ),
        migrations.AddIndex(
            model_name='traffic_data',
            index=models.Index(fields=['pid'], name='景区pid'),
        ),
        migrations.AddIndex(
            model_name='traffic_data',
            index=models.Index(fields=['date'], name='Day'),
        ),
        migrations.AddIndex(
            model_name='peopleflow',
            index=models.Index(fields=['pid'], name='ScencePid'),
        ),
        migrations.AddIndex(
            model_name='peopleflow',
            index=models.Index(fields=['date'], name='Day'),
        ),
    ]
