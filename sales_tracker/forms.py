from .models import MiningData, ContactData, LeadsData, OpportunityData, QuotesData
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

class TaskForm(forms.Form):
    # Priority choices
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]

    # Status choices
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    # Defining form fields
    subject = forms.CharField(
        max_length=200,
        label='Subject',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task subject'})
    )
    start_date = forms.DateField(
        label='Start Date',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    due_date = forms.DateField(
        label='Due Date',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        label='Priority',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter task description'}),
        label='Description'
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label='Status',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    related_to = forms.CharField(
        max_length=100,
        label='Related To',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter related entity'})
    )
    contacts = forms.EmailField(
        label='Contacts',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email contact'})
    )



