# Generated by Django 2.1.4 on 2018-12-22 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0016_journal_supplier'),
    ]

    operations = [
        migrations.CreateModel(
            name='income',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateTimeField()),
                ('sup', models.CharField(max_length=30)),
                ('item', models.CharField(max_length=30)),
                ('num', models.IntegerField()),
            ],
        ),
    ]
