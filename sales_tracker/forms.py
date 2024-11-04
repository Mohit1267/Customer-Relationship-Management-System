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

from django.core.exceptions import ValidationError

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
    email = forms.EmailField(
        max_length=255,
        label='Email',
        required=True
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Basic email validation example
        if not email.endswith('@example.com'):
            raise ValidationError('Please use an email address ending with @example.com')
        
        return email

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
            'email'
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
    email = forms.EmailField(
        max_length=255,
        label='Email',
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
            'email'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        # Basic email validation example
        if not email.endswith('@example.com'):
            raise ValidationError('Please use an email address ending with @example.com')
        
        return email


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

from django import forms

class InvoiceForm(forms.Form):
    title = forms.CharField(max_length=255)
    customer_name = forms.CharField(max_length=255)
    due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    assigned_to = forms.CharField(max_length=255)  # Placeholder for user field
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    
    invoice_number = forms.CharField(max_length=100, required=False)
    quotation_number = forms.CharField(max_length=100, required=False)
    invoice_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    status = forms.ChoiceField(choices=[('open', 'Open'), ('closed', 'Closed'), ('pending', 'Pending')], initial='open')
    
    account = forms.CharField(max_length=255)
    contact = forms.CharField(max_length=255)
    billing_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    shipping_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    
    currency = forms.CharField(max_length=10, initial='USD')
    line_items = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    
    total = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    discount = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    subtotal = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    shipping = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    adjustment = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    tax = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    grand_total = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    


from django import forms
from ckeditor.fields import RichTextField

class ComposeEmailForm(forms.Form):
    # 'template' is now a regular CharField and 'related_to' is a ChoiceField with specified options
    template = forms.CharField(
        max_length=255,
        required=False,
        label="Email Template",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    related_to = forms.ChoiceField(
        choices=[
             (' ', ' '),
            ('account', 'Account'),
            ('opportunity', 'Opportunity'),
            ('case', 'Case'),
            ('lead', 'Lead'),
            ('contact', 'Contact'),
            ('bug', 'Bug'),
            ('project', 'Project'),
            ('target', 'Target'),
            ('project_task', 'Project Task'),
            ('contract', 'Contract'),
            ('invoice', 'Invoice'),
            ('quote', 'Quote'),
            ('product', 'Product'),
        ],
        required=False,
        label="Related To",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    from_address = forms.EmailField(
        required=True,
        label="From",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    to_address = forms.EmailField(
        required=True,
        label="To",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    cc_address = forms.CharField(
        required=False,
        label="CC",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    bcc_address = forms.CharField(
        required=False,
        label="BCC",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    subject = forms.CharField(
        max_length=255,
        required=True,
        label="Subject",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    body = forms.CharField(
        required=True,
        label="Body",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6})
    )

    send_plain_text = forms.BooleanField(
        required=False,
        label="Send in Plain Text",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

from django import forms

class TargetsForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100, required=True)
    last_name = forms.CharField(label='Last Name', max_length=100, required=True)
    job_title = forms.CharField(label='Job Title', max_length=100, required=False)
    office_phone = forms.CharField(label='Office Phone', max_length=15, required=False)
    department = forms.CharField(label='Department', max_length=100, required=False)
    mobile = forms.CharField(label='Mobile', max_length=15, required=False)
    account_name = forms.CharField(label='Account Name', max_length=100, required=False)
    fax = forms.CharField(label='Fax', max_length=15, required=False)
    primary_address_street = forms.CharField(label='Street', max_length=255, required=False)
    primary_address_postal_code = forms.CharField(label='Postal Code', max_length=20, required=False)
    primary_address_city = forms.CharField(label='City', max_length=100, required=False)
    primary_address_state = forms.CharField(label='State', max_length=100, required=False)
    primary_address_country = forms.CharField(label='Country', max_length=100, required=False)
    other_address_street = forms.CharField(label='Street', max_length=255, required=False)
    other_address_postal_code = forms.CharField(label='Postal Code', max_length=20, required=False)
    other_address_city = forms.CharField(label='City', max_length=100, required=False)
    other_address_state = forms.CharField(label='State', max_length=100, required=False)
    other_address_country = forms.CharField(label='Country', max_length=100, required=False)
    email_address = forms.EmailField(label='Email Address', required=True)
    description = forms.CharField(label='Description', widget=forms.Textarea, required=False)
    assigned_to = forms.CharField(label='Assigned To', max_length=100, required=False)

# class InvoiceForm(forms.ModelForm):
#     class Meta:
#         # model = createInvoice
#         fields = [
#             'title', 'customer_name', 'due_date', 'assigned_to', 'description',
#             'invoice_number', 'quotation_number', 'invoice_date', 'status',
#             'account', 'contact', 'billing_address', 'shipping_address',
#             'currency', 'line_items', 'total', 'discount', 'subtotal', 
#             'shipping', 'adjustment', 'tax', 'grand_total'
#         ]
#         widgets = {
#             'due_date': forms.DateInput(attrs={'type': 'date'}),
#             'invoice_date': forms.DateInput(attrs={'type': 'date'}),
#             'description': forms.Textarea(attrs={'rows': 3}),
#             'billing_address': forms.Textarea(attrs={'rows': 2}),
#             'shipping_address': forms.Textarea(attrs={'rows': 2}),
#         }


    # You can add custom validation methods or additional features as needed


from django import forms

class TargetsListForm(forms.Form):
    name = forms.CharField(
        label="Name",
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'})
    )
    total_entries = forms.IntegerField(
        label="Total Entries",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter total entries'})
    )
    type = forms.ChoiceField(
        label="Type",
        choices=[
        ('default', 'Default'),
        ('seed', 'Seed'),
        ('suppression_list_by_domain', 'Suppression List - by Domain'),
        ('suppression_list_by_email', 'Suppression List - by Email'),
        ('suppression_list_by_id', 'Suppression List - by ID'),
        ('test', 'Test')
    ],
    widget=forms.Select(attrs={'class': 'form-control'})
)

    domain_name = forms.CharField(
        label="Domain Name",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter domain name'})
    )
    description = forms.CharField(
        label="Description",
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'})
    )


from django import forms
from .models import agentProjects

class AgentProjectsForm(forms.ModelForm):
    class Meta:
        model = agentProjects
        fields = [
            'name', 'status', 'draft', 'start_date', 'priority', 
            'end_date', 'consider_working_days', 'project_manager', 
            'project_template'
        ]
        
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AgentProjectsForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = "Name*"
        self.fields['status'].label = "Status"
        self.fields['draft'].label = "Draft"
        self.fields['start_date'].label = "Start Date*"
        self.fields['priority'].label = "Priority"
        self.fields['end_date'].label = "End Date*"
        self.fields['consider_working_days'].label = "Consider Working Days"
        self.fields['project_manager'].label = "Project Manager"
        self.fields['project_template'].label = "Project Template"

from django import forms
from .models import AgentTemplate  # Ensure this model exists and is correctly imported

class AgentTemplate(forms.ModelForm):
    class Meta:
        model = AgentTemplate  # Replace with the actual model name if different
        fields = [
            'template_name',
            'consider_working_days',
            'project_manager',
            'status',
            'priority'
        ]
        
        widgets = {
            'template_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter template name'}),
            'consider_working_days': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'project_manager': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project manager name'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom labels if necessary
        self.fields['template_name'].label = "Template Name"
        self.fields['consider_working_days'].label = "Consider Working Days"
        self.fields['project_manager'].label = "Project Manager"
        self.fields['status'].label = "Status"
        self.fields['priority'].label = "Priority"


# forms.py
from django import forms

class ContractForm(forms.Form):
    # Basic information section
    contract_title = forms.CharField(label="Contract Title", max_length=100, required=True)
    contract_value = forms.DecimalField(label="Contract Value", max_digits=10, decimal_places=2, required=True)
    start_date = forms.DateField(label="Start Date", widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    end_date = forms.DateField(label="End Date", widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    renewal_reminder_date = forms.DateField(label="Renewal Reminder Date", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    customer_schedule_date = forms.DateField(label="Customer Schedule Date", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    company_schedule_date = forms.DateField(label="Company Schedule Date", widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    description = forms.CharField(label="Description", widget=forms.Textarea, required=False)
    
    # Additional information section
    status = forms.ChoiceField(label="Status", choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], required=True)
    contact_manager = forms.CharField(label="Contact Manager", max_length=100, required=True)
    account = forms.CharField(label="Account", max_length=100, required=True)
    contact = forms.CharField(label="Contact", max_length=100, required=True)
    opportunity = forms.CharField(label="Opportunity", max_length=100, required=False)
    contact_type = forms.ChoiceField(label="Contact Type", choices=[('type1', 'Type 1'), ('type2', 'Type 2')], required=True)
    
    # Financial details section
    currency = forms.ChoiceField(label="Currency", choices=[('usd', 'USD'), ('eur', 'EUR')], required=True)
    total = forms.DecimalField(label="Total", max_digits=10, decimal_places=2, required=False)
    discount = forms.DecimalField(label="Discount", max_digits=10, decimal_places=2, required=False)
    subtotal = forms.DecimalField(label="Subtotal", max_digits=10, decimal_places=2, required=False)
    shipping = forms.DecimalField(label="Shipping", max_digits=10, decimal_places=2, required=False)
    shipping_tax = forms.DecimalField(label="Shipping Tax", max_digits=10, decimal_places=2, required=False)
    tax = forms.DecimalField(label="Tax", max_digits=10, decimal_places=2, required=False)
    grand_total = forms.DecimalField(label="Grand Total", max_digits=10, decimal_places=2, required=False)

    from django import forms

class CaseForm(forms.Form):
    CASE_STATES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    
    STATUS_OPTIONS = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    
    PRIORITY_OPTIONS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    case_number = forms.CharField(label="CASE NUMBER", required=True, max_length=50)
    priority = forms.ChoiceField(label="PRIORITY", choices=PRIORITY_OPTIONS, required=True)
    state = forms.ChoiceField(label="STATE", choices=CASE_STATES, required=True)
    status = forms.ChoiceField(label="STATUS", choices=STATUS_OPTIONS, required=True)
    type = forms.CharField(label="TYPE", required=True, max_length=50)
    account_name = forms.CharField(label="ACCOUNT NAME", required=True, max_length=100)
    subject = forms.CharField(label="SUBJECT", required=True, max_length=100)
    description = forms.CharField(label="DESCRIPTION", required=False, widget=forms.Textarea)
    resolution = forms.CharField(label="RESOLUTION", required=False, widget=forms.Textarea)
    assigned_to = forms.CharField(label="ASSIGNED TO", required=False, max_length=100)
    date_created = forms.DateField(label="DATE CREATED", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_modified = forms.DateField(label="DATE MODIFIED", required=False, widget=forms.DateInput(attrs={'type': 'date'}))


