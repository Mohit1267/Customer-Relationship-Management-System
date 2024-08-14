# Generated by Django 4.2.13 on 2024-07-08 07:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sales_tracker', '0011_alter_miningdata_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='miningdata',
            name='assigned_to',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='miningdata',
            name='date',
            field=models.DateField(),
        ),
    ]
