# Generated by Django 4.1 on 2022-11-16 18:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("travello", "0020_alter_transactions_date_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transactions",
            name="Date_Time",
            field=models.CharField(
                default=datetime.datetime(
                    2022, 11, 16, 18, 56, 22, 601153, tzinfo=datetime.timezone.utc
                ),
                max_length=19,
            ),
        ),
    ]
