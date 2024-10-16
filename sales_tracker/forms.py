from .models import MiningData, ContactData, LeadsData, OpportunityData, QuotesData
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


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


class AccountForm(forms.Form):
    # Left Column Fields
    Name = forms.CharField(max_length=100, label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Website = forms.URLField(label='Website', widget=forms.URLInput(attrs={'class': 'form-control'}))
    Email_Address = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    Billing_Address = forms.CharField(max_length=255, label='Billing Address', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Billing_Street = forms.CharField(max_length=255, label='Billing Street', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Billing_Postal_Code = forms.CharField(max_length=20, label='Billing Postal Code', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Billing_City = forms.CharField(max_length=100, label='Billing City', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Billing_State = forms.CharField(max_length=100, label='Billing State', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Billing_Country = forms.CharField(max_length=100, label='Billing Country', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label='Description')
    Assigned_To = forms.CharField(max_length=100, label='Assigned To', widget=forms.TextInput(attrs={'class': 'form-control'}))

    # Right Column Fields
    Shipping_Address = forms.CharField(max_length=255, label='Shipping Address', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Shipping_Street = forms.CharField(max_length=255, label='Shipping Street', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Shipping_Postal_Code = forms.CharField(max_length=20, label='Shipping Postal Code', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Shipping_City = forms.CharField(max_length=100, label='Shipping City', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Shipping_State = forms.CharField(max_length=100, label='Shipping State', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Shipping_Country = forms.CharField(max_length=100, label='Shipping Country', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Type = forms.CharField(max_length=50, label='Type', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Annual_Revenue = forms.DecimalField(max_digits=10, decimal_places=2, label='Annual Revenue', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Member_Of = forms.CharField(max_length=100, label='Member Of', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Campaign = forms.CharField(max_length=100, label='Campaign', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Industry = forms.CharField(max_length=100, label='Industry', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Employees = forms.IntegerField(label='Employees', widget=forms.NumberInput(attrs={'class': 'form-control'}))



TYPE_CHOICES = [
    ('option1', 'Option 1'),
    ('option2', 'Option 2'),
    ('option3', 'Option 3'),
]

class Accountform(forms.Form):
    type = forms.ChoiceField(
        choices=TYPE_CHOICES, 
        label='Type', 
        widget=forms.Select(attrs={'class': 'form-control'})
    )


    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'Name',
            'Website',
            'Email_Address',
            'Billing_Address',
            'Billing_Street',
            'Billing_Postal_Code',
            'Billing_City',
            'Billing_State',
            'Billing_Country',
            'Description',
            'Assigned_To',
            'Shipping_Address',
            'Shipping_Street',
            'Shipping_Postal_Code',
            'Shipping_City',
            'Shipping_State',
            'Shipping_Country',
            'Type',
            'Annual_Revenue',
            'Member_Of',
            'Campaign',
            'Industry',
            'Employees'
        )

