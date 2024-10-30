from .models import MiningData, ContactData, LeadsData, OpportunityData, QuotesData, Document, Schedule_Meeting,Schedule_Calling, Task, agentNotes
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from .models import Schedule_Calling
from datetime import timedelta
from crispy_forms.layout import Layout, Submit, Row, Column




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


from django import forms
from .models import NewPasswords

class PasswordForm(forms.ModelForm):
    class Meta:
        model = NewPasswords
        fields = ['Minor_password', 'Sales_password', 'Admin_password']


class SortForm(forms.Form):
    select = forms.ChoiceField(choices=MY_CHOICES, label='Select an option')

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['subject', 'start_date', 'due_date', 'priority', 'description', 'status', 'related_to', 'contacts']
        
        # Custom widgets for form fields
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task subject'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter task description'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'related_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Related to (optional)'}),
            'contacts': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # Customizing the labels or adding help texts if needed
        self.fields['subject'].label = "Task Subject"
        self.fields['contacts'].help_text = "Hold Ctrl to select multiple contacts"



class AccountForm(forms.Form):
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




class DocumentForm(forms.ModelForm):
    # Custom widgets can be defined here if needed
    publish_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    expiration_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    
    class Meta:
        model = Document
        fields = ['file_name', 'document_name', 'document_type', 'publish_date', 'category',
                  'description', 'status', 'revision', 'template', 'expiration_date',
                  'subcategory', 'related_document', 'assigned_to']

        widgets = {
            'file_name': forms.TextInput(attrs={'class': 'form-control'}),
            'document_name': forms.TextInput(attrs={'class': 'form-control'}),
            'document_type': forms.Select(attrs={'class': 'form-control'}),  # Assuming this is a choice field
            'category': forms.Select(attrs={'class': 'form-control'}),  # Assuming this is a choice field
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),  # Assuming this is a choice field
            'revision': forms.TextInput(attrs={'class': 'form-control'}),
            'template': forms.TextInput(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),  # Assuming this is a choice field
            'related_document': forms.TextInput(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),  # Assuming this is a choice field
        }


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
    contact = forms.CharField(
    label='Contact',
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
            'contact',  
        ]



class agentcalling(forms.ModelForm):

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

    contact = forms.IntegerField(
        label='Contact',
        required=True
    )
    class Meta:
        model = Schedule_Calling  # Replace with your actual model name
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
            'contact',
        ]


import re  # Make sure to import the re module
from django import forms
from .models import DailySalesReport  # Assuming you have a DailySalesReport model

class DailySalesReportForm(forms.ModelForm):
    class Meta:
        model = DailySalesReport  # Specify your model
        fields = [
            'name',
            'customer_type',
            'call_type',
            'date',
            'time',
            'item_number',
            'item_name',
            'item_description',
            'unit_cost',
            'quantity',
            'amount',
            'tax_rate',
            'tax',
            'total',
            'notes',  # Include notes in the fields
        ]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match("^[A-Za-z ]+$", name):
            raise forms.ValidationError("Name can only contain alphabets and spaces.")
        return name

    def clean_customer_type(self):
        customer_type = self.cleaned_data.get('customer_type')
        if not re.match("^[A-Za-z ]+$", customer_type):
            raise forms.ValidationError("Customer Type can only contain alphabets and spaces.")
        return customer_type

    def clean_call_type(self):
        call_type = self.cleaned_data.get('call_type')
        if not re.match("^[A-Za-z ]+$", call_type):
            raise forms.ValidationError("Call Type can only contain alphabets and spaces.")
        return call_type

    def clean_item_number(self):
        item_number = self.cleaned_data.get('item_number')
        if not re.match("^\d+$", item_number):  # Ensure only numbers
            raise forms.ValidationError("Item Number can only contain digits.")
        return item_number

    def clean_item_name(self):
        item_name = self.cleaned_data.get('item_name')
        if not re.match("^[A-Za-z0-9 ]+$", item_name):  # Allow alphabets and numbers
            raise forms.ValidationError("Item Name can only contain alphabets and numbers.")
        return item_name

    def clean_item_description(self):
        item_description = self.cleaned_data.get('item_description')
        if not re.match("^[A-Za-z0-9 ]+$", item_description):  # Allow alphabets and numbers
            raise forms.ValidationError("Item Description can only contain alphabets and numbers.")
        return item_description

    def clean_unit_cost(self):
        unit_cost = self.cleaned_data.get('unit_cost')
        if unit_cost is None or not isinstance(unit_cost, (int, float)) or unit_cost < 0:
            raise forms.ValidationError("Unit Cost must be a positive number.")
        return unit_cost

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or not isinstance(quantity, (int, float)) or quantity < 0:
            raise forms.ValidationError("Quantity must be a positive number.")
        return quantity

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is None or not isinstance(amount, (int, float)) or amount < 0:
            raise forms.ValidationError("Amount must be a positive number.")
        return amount

    def clean_tax_rate(self):
        tax_rate = self.cleaned_data.get('tax_rate')
        if tax_rate is None or not isinstance(tax_rate, (int, float)) or tax_rate < 0:
            raise forms.ValidationError("Tax Rate must be a positive number.")
        return tax_rate

    def clean_tax(self):
        tax = self.cleaned_data.get('tax')
        if tax is None or not isinstance(tax, (int, float)) or tax < 0:
            raise forms.ValidationError("Tax must be a positive number.")
        return tax

    def clean_total(self):
        total = self.cleaned_data.get('total')
        if total is None or not isinstance(total, (int, float)) or total < 0:
            raise forms.ValidationError("Total must be a positive number.")
        return total

    def clean_notes(self):
        notes = self.cleaned_data.get('notes')
        if notes is not None and not re.match("^[A-Za-z0-9 ]*$", notes):  # Allow alphabets and numbers
            raise forms.ValidationError("Notes can only contain alphabets, numbers, and spaces.")
        return notes


class NoteForm(forms.ModelForm):
    class Meta:
        model = agentNotes
        fields = ['subject', 'contact', 'attachment', 'note', 'related_to']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter subject'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact name'}),
            'attachment': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your note'}),
            'related_to': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Related to'}),
        }

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'title', 'customer_name', 'due_date', 'assigned_to', 'description',
            'invoice_number', 'quotation_number', 'invoice_date', 'status',
            'account', 'contact', 'billing_address', 'shipping_address',
            'currency', 'line_items', 'total', 'discount', 'subtotal', 
            'shipping', 'adjustment', 'tax', 'grand_total'
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'invoice_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'billing_address': forms.Textarea(attrs={'rows': 2}),
            'shipping_address': forms.Textarea(attrs={'rows': 2}),
        }