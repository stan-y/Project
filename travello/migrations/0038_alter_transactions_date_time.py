# Generated by Django 4.1.3 on 2022-11-20 14:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travello', '0037_alter_transactions_date_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactions',
            name='Date_Time',
            field=models.CharField(default=datetime.datetime(2022, 11, 20, 14, 32, 41, 496816, tzinfo=datetime.timezone.utc), max_length=150),
        ),
    ]
