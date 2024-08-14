# Generated by Django 5.0.7 on 2024-08-14 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_tracker', '0023_alter_contactdata_contact_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallingAgent',
            fields=[
                ('calling_agent_id', models.AutoField(primary_key=True, serialize=False)),
                ('calling_agent_name', models.CharField(max_length=50)),
                ('calling_agent_email', models.EmailField(max_length=50)),
                ('calling_agent_contact', models.CharField(max_length=15)),
                ('calling_agent_call_date', models.DateField()),
            ],
            options={
                'db_table': 'CallingAgent',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CallingAgentProxy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'CallingAgent',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='contactdata',
            name='calling_agent',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sales_tracker.callingagent'),
        ),
    ]
