# Generated by Django 2.1.4 on 2018-12-22 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0012_journal_request'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_bin',
            name='pay_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='journal_request',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
