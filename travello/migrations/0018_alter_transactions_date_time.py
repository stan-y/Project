# Generated by Django 4.1 on 2022-11-08 14:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("travello", "0017_alter_transactions_date_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transactions",
            name="Date_Time",
            field=models.CharField(
                default=datetime.datetime(
                    2022, 11, 8, 14, 7, 26, 151640, tzinfo=datetime.timezone.utc
                ),
                max_length=19,
            ),
        ),
    ]
