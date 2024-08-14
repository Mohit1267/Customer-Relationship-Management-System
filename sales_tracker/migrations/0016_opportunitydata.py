# Generated by Django 4.2.13 on 2024-07-10 10:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sales_tracker', '0015_rename_leaddata_leadsdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpportunityData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opportunity_name', models.CharField(max_length=50)),
                ('amount', models.IntegerField()),
                ('sales_stage', models.CharField(choices=[('prospecting', 'Prospecting'), ('qualification', 'Qualification'), ('needs', 'Needs'), ('value_proposition', 'Value Proposition'), ('identifying_decision_makers', 'Identifying Decision Makers'), ('preception_Analysis', 'Perception Analysis'), ('Proposal-price_quote', 'Proposal/Prise Quote'), ('negotiation-review', 'Negotiation/Review'), ('closed_won', 'Closed Won'), ('closed_lost', 'Closed lost')], max_length=50)),
                ('probability', models.IntegerField()),
                ('next_step', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('expected_close_date', models.DateField()),
                ('lead_sourse', models.CharField(max_length=50)),
                ('date', models.DateField(default='2000-10-10')),
                ('assigned_to', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sales_tracker.leadsdata')),
            ],
        ),
    ]
