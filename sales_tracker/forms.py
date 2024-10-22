from .models import MiningData, ContactData, LeadsData, OpportunityData, QuotesData, Document, Schedule_Meeting,Schedule_Calling, Task
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


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['subject', 'start_date', 'due_date', 'priority', 'description', 'status', 'related_to', 'contacts']  # List all required fields

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

# Define choices for Type, Campaign, and Industry
TYPE_CHOICES = [
    ('select', 'Select'),
    ('analyst', 'Analyst'),
    ('competitor', 'Competitor'),
    ('customer', 'Customer'),
    ('integrator', 'Integrator'),
    ('investor', 'Investor'),
    ('partner', 'Partner'),
    ('press', 'Press'),
    ('prospect', 'Prospect'),
    ('reseller', 'Reseller'),
    ('other', 'Other')]

CAMPAIGN_CHOICES = [
    
]

INDUSTRY_CHOICES = [
     ('apparel', 'Apparel'),
    ('banking', 'Banking'),
    ('biotechnology', 'Biotechnology'),
    ('chemicals', 'Chemicals'),
    ('communications', 'Communications'),
    ('construction', 'Construction'),
    ('consulting', 'Consulting'),
    ('education', 'Education'),
    ('electronics', 'Electronics'),
    ('energy', 'Energy'),
    ('engineering', 'Engineering'),
    ('entertainment', 'Entertainment'),
    ('environmental', 'Environmental'),
    ('finance', 'Finance'),
    ('government', 'Government'),
    ('healthcare', 'Healthcare'),
    ('hospitality', 'Hospitality'),
    ('insurance', 'Insurance'),
    ('machinery', 'Machinery'),
    ('manufacturing', 'Manufacturing'),
    ('media', 'Media'),
    ('not_for_profit', 'Not For Profit'),
    ('recreation', 'Recreation'),
    ('retail', 'Retail'),
    ('shipping', 'Shipping'),
    ('technology', 'Technology'),
    ('telecommunications', 'Telecommunications'),
    ('transportation', 'Transportation'),
    ('utilities', 'Utilities'),
    ('other', 'Other'),
]

class AccountForm(forms.Form):
    # Basic Information
    Name = forms.CharField(max_length=100, label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Website = forms.URLField(label='Website', widget=forms.URLInput(attrs={'class': 'form-control'}))
    Email_Address = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    # Billing Information
    Billing_Address = forms.CharField(max_length=255, label='Billing Address', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Billing_Street = forms.CharField(max_length=255, label='Billing Street', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Billing_Postal_Code = forms.CharField(max_length=20, label='Billing Postal Code', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Billing_City = forms.CharField(max_length=100, label='Billing City', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Billing_State = forms.CharField(max_length=100, label='Billing State', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Billing_Country = forms.CharField(max_length=100, label='Billing Country', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    # Description and Assignment
    Description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), label='Description')
    Assigned_To = forms.CharField(max_length=100, label='Assigned To', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    # Shipping Information
    Shipping_Address = forms.CharField(max_length=255, label='Shipping Address', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Shipping_Street = forms.CharField(max_length=255, label='Shipping Street', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Shipping_Postal_Code = forms.CharField(max_length=20, label='Shipping Postal Code', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Shipping_City = forms.CharField(max_length=100, label='Shipping City', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Shipping_State = forms.CharField(max_length=100, label='Shipping State', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Shipping_Country = forms.CharField(max_length=100, label='Shipping Country', widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    # Dropdowns for Type, Campaign, and Industry
    Type = forms.ChoiceField(choices=TYPE_CHOICES, label='Type', widget=forms.Select(attrs={'class': 'form-control'}))
    Campaign = forms.ChoiceField(choices=CAMPAIGN_CHOICES, label='Campaign', widget=forms.Select(attrs={'class': 'form-control'}))
    Industry = forms.ChoiceField(choices=INDUSTRY_CHOICES, label='Industry', widget=forms.Select(attrs={'class': 'form-control'}))
    
    # Other Information
    Annual_Revenue = forms.DecimalField(max_digits=10, decimal_places=2, label='Annual Revenue', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    Member_Of = forms.CharField(max_length=100, label='Member Of', widget=forms.TextInput(attrs={'class': 'form-control'}))
    Employees = forms.IntegerField(label='Employees', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    # Form Initialization
    def _init_(self, *args, **kwargs):
        super(AccountForm, self)._init_(*args, **kwargs)
        # Use Crispy Forms' FormHelper for layout management
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
            'Campaign',
            'Industry',
            'Annual_Revenue',
            'Member_Of',
            'Employees'
        )
        # Add submit button
        self.helper.add_input(Submit('submit', 'Create Account'))



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



# class agentcalling(forms.ModelForm):
#     start_date = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         label='Start Date',
#         required=True
#     )
#     end_date = forms.DateField(
#         widget=forms.DateInput(attrs={'type': 'date'}),
#         label='End Date',
#         required=True
#     )
#     duration = forms.CharField(
#         # widget=forms.TextInput(attrs={'placeholder': 'e.g., 2 hours, 30 minutes'}),
#         max_length=255,
#         label='Duration',
#         required=False,
#         help_text='Enter the duration (e.g., 2 hours, 30 minutes)'
#     )
#     frequency = forms.ChoiceField(
#         choices=[
#             ('daily', 'Daily'),
#             ('weekly', 'Weekly'),
#             ('monthly', 'Monthly'),
#             ('yearly', 'Yearly'),
#         ],
#         label='Frequency',
#         required=True
#     )
#     start_time = forms.TimeField(
#         widget=forms.TimeInput(attrs={'type': 'time'}),
#         label='Start Time',
#         required=True
#     )
#     end_time = forms.TimeField(
#         widget=forms.TimeInput(attrs={'type': 'time'}),
#         label='End Time',
#         required=True
#     )

#     subject = forms.CharField(
#         max_length=255,
#         label='Subject',
#         required=True
#     )

#     related_to = forms.ChoiceField(
#         choices=[
#             ('', 'Select an option'),
#             ('Client', 'Client'),
#             ('Lead', 'Lead'),
#             ('Opportunity', 'Opportunity'),
#             ('Account', 'Account'),
#         ],
#         label='Related To',
#         required=True
#     )

#     assigned_to = forms.ChoiceField(
#         choices=[
#         ('', 'Select an option'),
#         ('Client', 'Client'),
#         ('Lead', 'Lead'),
#         ('Opportunity', 'Opportunity'),
#         ('Account', 'Account'),
#     ],
#         label='Assigned To',
#         required=True
#     )

#     notification = forms.CharField(
#         max_length=255,
#         label='Notification',
#         required=True
#     )
#     contact = forms.IntegerField(
#         label='Contact Number',
#         required=True
#     )

#     class Meta:
#         model = Schedule_Calling
#         fields = [
#             'start_date',
#             'end_date',
#             'duration',
#             'frequency',
#             'start_time',
#             'end_time',
#             'subject',
#             'related_to',
#             'assigned_to',
#             'notification',
#             'contact',
#             'notes',
#             'reason',
#         ]


# class agentcalling(forms.ModelForm):
#     start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Start Date', required=True)
#     end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='End Date', required=True)
#     duration = forms.CharField(max_length=255, label='Duration', required=False, help_text='Enter the duration (e.g., 2 hours, 30 minutes)')
#     frequency = forms.ChoiceField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'Yearly')], label='Frequency', required=True)
#     start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='Start Time', required=True)
#     end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label='End Time', required=True)
#     subject = forms.CharField(max_length=255, label='Subject', required=True)
#     related_to = forms.ChoiceField(choices=[('', 'Select an option'), ('Client', 'Client'), ('Lead', 'Lead'), ('Opportunity', 'Opportunity'), ('Account', 'Account')], label='Related To', required=True)
#     assigned_to = forms.ChoiceField(choices=[('', 'Select an option'), ('Client', 'Client'), ('Lead', 'Lead'), ('Opportunity', 'Opportunity'), ('Account', 'Account')], label='Assigned To', required=True)
#     notification = forms.CharField(max_length=255, label='Notification', required=True)
#     contact = forms.IntegerField(label='Contact Number', required=True)
#     notes = forms.CharField(max_length=255, label='Notes', required=True)
#     reason = forms.CharField(max_length=255, label='Reason', required=True)

#     class Meta:
#         model = Schedule_Calling
#         fields = ['start_date', 'end_date', 'duration', 'frequency', 'start_time', 'end_time', 'subject', 'related_to', 'assigned_to', 'notification', 'contact', 'notes', 'reason']


    # def clean_duration(self):
    #     duration = self.cleaned_data.get('duration')
    #     if duration:
    #         return timedelta(hours=duration.hour, minutes=duration.minute)
    #     return duration


class ScheduleCallingForm(forms.ModelForm):
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
        label='Subject',
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
    contact = forms.IntegerField(
        label='Contact',
        required=True
    )
    notes = forms.CharField(
        max_length=255,
        label='Notes',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )
    reason = forms.CharField(
        max_length=255,
        label='Reason',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3})
    )

    class Meta:
        model = Schedule_Calling
        fields = [
            'start_date', 'end_date', 'duration', 'frequency', 'start_time', 
            'end_time', 'subject', 'related_to', 'assigned_to', 
            'notification', 'contact', 'notes', 'reason'
        ]

    def _init_(self, *args, **kwargs):
        super(ScheduleCallingForm, self)._init_(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('start_date', css_class='form-group col-md-6 mb-0'),
                Column('end_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_time', css_class='form-group col-md-6 mb-0'),
                Column('end_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'duration',
            'frequency',
            'subject',
            'related_to',
            'assigned_to',
            'notification',
            'contact',
            'notes',
            'reason',
            Submit('submit', 'Save')
        )

        

# from django import forms
# from .models import Task

# class TaskForm(forms.ModelForm):
#     # Fields definition
#     contact = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Contact Name'}))
#     subject = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter Subject'}))
#     attachment = forms.FileField(required=False)  # Optional attachment
#     note = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter Notes'}), required=False)
#     related_to = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter Related To'}))

#     class Meta:
#         model = Task  # Use your actual model name
#         fields = ['contact', 'subject', 'attachment', 'note', 'related_to']
# =======
            

