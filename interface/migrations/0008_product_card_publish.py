# Generated by Django 2.1.4 on 2018-12-20 18:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0007_auto_20181220_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_card',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
