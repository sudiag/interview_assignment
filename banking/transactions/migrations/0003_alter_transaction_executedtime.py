# Generated by Django 3.2.9 on 2021-11-08 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20211106_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='executedTime',
            field=models.DateTimeField(auto_now=True, default="2021-11-06T19:36:02.253326Z"),
            preserve_default=False,
        ),
    ]
