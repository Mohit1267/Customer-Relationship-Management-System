# Generated by Django 4.1.5 on 2024-06-13 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_tracker', '0007_timer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Timer',
        ),
        migrations.AlterField(
            model_name='miningdata',
            name='date',
            field=models.DateField(default='2024-06-13'),
        ),
    ]
