# Generated by Django 2.2.1 on 2019-05-12 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebView', '0002_auto_20190512_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peopleflow',
            name='date',
            field=models.DateField(verbose_name='日期'),
        ),
    ]
