# Generated by Django 4.2.13 on 2024-06-18 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_profile_id_alter_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='can_login',
            field=models.BooleanField(default=True),
        ),
    ]
