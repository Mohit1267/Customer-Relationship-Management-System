from .models import MiningData, ContactData, LeadsData, OpportunityData, QuotesData, Schedule_Meeting
from django import forms

class MiningForm(forms.ModelForm):
    class Meta:
        model = MiningData
        fields = "__all__"
        exclude = ["date", "assigned_to" ]

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactData
        fields = "__all__"
        exclude = ["date", "assigned_to" ]

# class LeadForm(forms.ModelForm):
#     class Meta:
#         model = LeadsData
#         fields = "__all__"
#         exclude = ["date", "assigned_to" ]

class LeadForm(forms.ModelForm):
    lead_name = forms.ModelChoiceField(
        queryset=MiningData.objects.all(),
        to_field_name="organisation_name",
        empty_label="Select Organization",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = LeadsData
        fields = "__all__"
        exclude = ["date", "assigned_to"]

class OpportunityForm(forms.ModelForm):
    class Meta:
        model = OpportunityData
        fields = "__all__"
        exclude = ["date", "assigned_to" ]

class QuoteForm(forms.ModelForm):
    class Meta:
        model = QuotesData
        fields = "__all__"
        exclude = ["date", "assigned_to" ]

MY_CHOICES = (
    ('day', 'day'),
    ('week', 'week'),
    ('month', 'month'),
)

class SortForm(forms.Form):
    select = forms.ChoiceField(choices=MY_CHOICES, label='Select an option')


class agentmeeting(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Start Date',
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='End Date',
        required=True
    )
    duration = forms.CharField(
        max_length=255,
        label='Duration',
        required=False,
        help_text='Enter the duration (e.g., 2 hours, 30 minutes)'
    )
    frequency = forms.ChoiceField(
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
        ],
        label='Frequency',
        required=True
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='Start Time',
        required=True
    )
    end_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label='End Time',
        required=True
    )

    subject = forms.CharField(
        max_length=255,
        label='subject',
        required=True
    )

     
    related_to = forms.ChoiceField(
        choices=[
        ('', 'Select an option'),
        ('Client', 'Client'),
        ('Lead', 'Lead'),
        ('Opportunity', 'Opportunity'),
        ('Account', 'Account'),
    ],
        
        label='Related To',
        required=True
    )

    assigned_to = forms.ChoiceField(
        choices=[
        ('', 'Select an option'),
        ('Client', 'Client'),
        ('Lead', 'Lead'),
        ('Opportunity', 'Opportunity'),
        ('Account', 'Account'),
    ],
        label='Assigned To',
        required=True
    )

    notification = forms.CharField(
        max_length=255,
        label='Notification',
        required=True
    )

    notes = forms.CharField(
        max_length=255,
        label='note',
        required=True
    )
    class Meta:
        model = Schedule_Meeting  # Replace with your actual model name
        fields = [
           'start_date',
            'end_date',
            'duration',
            'frequency',
            'start_time',
            'end_time',
            'subject',
            'related_to',
            'assigned_to',
            'notification',
            'notes',
        ]


