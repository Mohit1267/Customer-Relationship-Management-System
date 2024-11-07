from django.db import models
from django.conf import settings
import datetime

from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from users.models import RegisterUser, Profile




class CallingAgent(models.Model):
    calling_agent_id = models.AutoField(primary_key=True)
    calling_agent_name = models.CharField(max_length=50)
    calling_agent_email = models.EmailField(max_length=50)
    calling_agent_contact = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'CallingAgent' 
    def __str__(self):
        return f"{self.calling_agent_id}"


class MiningData(models.Model):
    organisation_name = models.CharField( max_length=50, primary_key=True)
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    customer_address = models.TextField()
    customer_contact_number = models.CharField(max_length=15)
    customer_mobile_number = models.CharField(max_length=15)
    customer_email = models.EmailField()
    company_revenue = models.CharField( max_length=50)
    company_emp_size = models.IntegerField()
    customer_offering = models.CharField(max_length=30)
    competition_of_AT = models.CharField(max_length=50)
    stock_market_registered = models.CharField(max_length=20)
    influncer = models.BooleanField()
    desition_maker = models.BooleanField()
    IT_spending_budget = models.CharField(max_length=30)
    source_of_data_mining = models.CharField(max_length=50)
    date = models.DateField()
    assigned_to = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default=1, null = True, blank = True)
    created_by = models.ForeignKey(RegisterUser,on_delete=models.CASCADE, related_name='mining_data',null=True,blank = True)
    state = models.CharField(max_length=50,default='MP')
    city = models.CharField(max_length=50,default='Indore')
    region = models.CharField(max_length=50, default='North')


    def __str__(self):
        return f"{self.organisation_name}"
    
class ContactData(models.Model):
    first_name = models.CharField( max_length=50)
    last_name = models.CharField( max_length=50)
    email_id = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15)
    job_title = models.CharField( max_length=50)
    address = models.TextField( )
    date = models.DateField(default="2000-10-10")
    organization = models.ForeignKey(MiningData, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default=1)
    created_by = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, related_name='calling_data',default=1)
    # calling_agent = foreign key to agent profile to which call is assigned
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class LeadsData(models.Model):
    LEAD_STATUS_CHOICES = [
       
        ('HOT', 'Hot'),
        ('COLD', 'Cold'),
        ('MILD', 'Mild'),
    ]
    lead_name = models.CharField( max_length=50)
    first_name = models.CharField( max_length=50)
    last_name = models.CharField( max_length=50)
    email_id = models.EmailField()
    contact_number = models.CharField(max_length=15)
    job_title = models.CharField( max_length=50)
    address = models.TextField( )
    date = models.DateField(default="2000-10-10")
    contact_link = models.ForeignKey(ContactData, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default=1)
    status = models.CharField(max_length=10, choices=LEAD_STATUS_CHOICES)
    created_by = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, related_name='leads_by',default=11)
    remarks = models.TextField(  )
    nextdate = models.DateField()
    
    def __str__(self):
        return f"{self.lead_name}"
    
class OpportunityData(models.Model):
    opportunity_name =  models.CharField( max_length=50)
    amount = models.IntegerField()
    sales_stage = models.CharField(max_length=50, choices=(
        ('prospecting', 'Prospecting'),
        ('qualification', 'Qualification'),
        ('needs', 'Needs'),
        ('value proposition', 'Value Proposition'),
        ('identifying decision makers', 'Identifying Decision Makers'),
        ('preception Analysis', 'Perception Analysis'),
        ('Proposal/price quote', 'Proposal/Prise Quote'),
        ('negotiation/review', 'Negotiation/Review'),
        ('closed won', 'Closed Won'),
        ('closed lost', 'Closed lost'),
    ))
    probability = models.IntegerField()
    next_step = models.CharField(max_length=50)
    description = models.TextField()
    expected_close_date = models.DateField()
    lead_source = models.CharField(max_length=50)
    date = models.DateField(default="2000-10-10")
    lead = models.ForeignKey(LeadsData, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default=1)

class QuotesData(models.Model):
    title = models.CharField(max_length= 50)
    valid_until = models.DateField()
    approval_status = models.CharField(max_length=50, choices=(
        ('approved', 'Approved'),
        ('not approved', 'Not Approved'),
    ))

    opportunity = models.ForeignKey(OpportunityData, on_delete=models.CASCADE)
    quote_stage = models.CharField(max_length=50, choices=(
        ('draft', 'Draft'),
        ('negotiation', 'Negotiation'), 
        ('delivered', 'delivered'),
        ('on hold', 'On Hold'),
        ('confirmed', 'Confirmed'),
        ('closed Accepted', 'Closed Accepted'),
        ('closed lost', 'Closed Lost'),
        ('closed dead', 'Closed Dead'),
    ))
    invoice_status = models.CharField(max_length=50, choices=(
        ('not invoiced', 'Not Invoiced'),
        ('invoiced', 'Invoiced'),
    ))
    approval_issues_description = models.TextField(null=True, blank=True)

    lead_source = models.CharField(max_length= 50)
    account = models.CharField(max_length= 50)
    contact = models.CharField(max_length= 50,null = True)
    billing_address = models.TextField()
    shipping_address = models.TextField()

    total = models.CharField(max_length=50)
    discount = models.CharField(max_length=50)
    sub_total = models.CharField(max_length=50)
    shipping = models.CharField(max_length=50)
    shipping_tax = models.CharField(max_length=50)
    tax = models.CharField(max_length=50)
    grandtotal = models.CharField(max_length=50)
    date = models.DateField()
    assigned_to = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default=1)


class Location(models.Model):
   
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Account(models.Model):
    
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    email_address = models.EmailField()   
    billing_address = models.CharField(max_length=255)
    billing_street = models.CharField(max_length=255)
    billing_postal_code = models.CharField(max_length=20)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_country = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_street = models.CharField(max_length=255, blank=True, null=True)
    shipping_postal_code = models.CharField(max_length=20, blank=True, null=True)
    shipping_city = models.CharField(max_length=100, blank=True, null=True)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_country = models.CharField(max_length=100, blank=True, null=True)
    

    type = models.CharField(max_length=50,choices=(
        ('option1', 'Option 1'),
        ('option2', 'Option 2'),
        ('option3', 'Option 3'),
    ))

    annual_revenue = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    member_of = models.CharField(max_length=100, blank=True, null=True)
    campaign = models.CharField(max_length=100, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    employees = models.IntegerField(blank=True, null=True)
    # Timestamps
    created_at = models.DateTimeField(default=datetime.datetime.now)  # Temporary for migration

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



password_regex = RegexValidator(
     regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
 
    message="Password must contain at least 8 characters, one uppercase, one lowercase, one number, and one special character."
)

class NewPasswords(models.Model):
    Minor_password = models.CharField(
        max_length=128,
        validators=[password_regex],
        help_text="Password must be at least 8 characters long and include an uppercase, lowercase, number, and special character."
    )
 
    Sales_password = models.CharField(
        max_length=128,
        validators=[password_regex],
        help_text="Password must be at least 8 characters long and include an uppercase, lowercase, number, and special character."
    )

    Admin_password = models.CharField(
        max_length=128,
        validators=[password_regex],
        help_text="Password must be at least 8 characters long and include an uppercase, lowercase, number, and special character."
    )



 
class Schedule_Meeting(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.DurationField()
    frequency = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=255)
    related_to = models.CharField(max_length=255)
    assigned_to = models.CharField(max_length=255)
    notification = models.CharField(max_length=255)
    notes = models.CharField(max_length=255, null = True)
    contact= models.EmailField(null = True)
    temp = models.CharField(max_length=233, null = True,  blank = True)


    def str(self):
        return f"Schedule from {self.start_date} to {self.end_date}"

class Schedule_Calling(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    duration = models.DurationField()
    frequency = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.CharField(max_length=255)
    related_to = models.CharField(max_length=255)
    assigned_to = models.CharField(max_length=255)
    notification = models.CharField(max_length=255)
    contact= models.IntegerField(null = True)
    notes = models.CharField(max_length=255, null = True)
    reason = models.CharField(max_length=255, null = True)

    def str(self):
        return f"Schedule_Calling from {self.start_date} to {self.end_date}"
    

class Document(models.Model):
    FILE_TYPES = (
        ('pdf', 'PDF'),
        ('doc', 'Word Document'),
        ('xls', 'Excel Spreadsheet'),
    )

    STATUSES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    )

    CATEGORIES = (
        ('legal', 'Legal'),
        ('finance', 'Finance'),
        ('technical', 'Technical'),
    )
    
    SUBCATEGORIES = (
        ('subcat1', 'Subcategory 1'),
        ('subcat2', 'Subcategory 2'),
    )

    file_name = models.CharField(max_length=255)
    document_name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=10, choices=FILE_TYPES)
    publish_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUSES)
    revision = models.CharField(max_length=10)
    template = models.CharField(max_length=255, null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORIES)
    related_document = models.CharField(max_length=255, null=True, blank=True)
    assigned_to = models.ForeignKey(RegisterUser, on_delete=models.SET_NULL, null=True)

    def _str_(self):
        return self.document_name
    notes = models.CharField(max_length=255,  null=True, blank=True)

    reason = models.CharField(max_length=255,  null=True, blank=True)

    
    def __str__(self):
        return f"Schedule_Calling from {self.start_date} to {self.end_date}"

class Task(models.Model):
    TASK_PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    TASK_STATUS_CHOICES = [
        ('-------', '-------'),
        ('not started ', 'Not Started '),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('pending_input', 'Pending Input'),
        ('deferred ', 'Deferred '),
    ]

    subject = models.CharField(max_length=100)

    start_date = models.DateField()
    due_date = models.DateField()
    priority = models.CharField(max_length=6, choices=TASK_PRIORITY_CHOICES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='open')

    related_to = models.CharField(max_length=100, blank=True, null=True)  
    contacts = models.ManyToManyField('ContactData', related_name='tasks')
    def _str_(self):
        return self.subject

class DailySalesReport(models.Model):
    name = models.CharField(max_length=100)
    customer_type = models.CharField(max_length=50)
    call_type = models.CharField(max_length=50)
    date = models.DateField()
    time = models.TimeField()
    item_number = models.CharField(max_length=50)
    item_name = models.CharField(max_length=100)
    item_description = models.TextField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)  

    def __str__(self):
        return f"{self.name} - {self.date} - {self.item_name}"

    class Meta:
        verbose_name = "Daily Sales Report"
        verbose_name_plural = "Daily Sales Reports"
        ordering = ['-date']  




class agentNotes(models.Model):
    RELATED_TO_CHOICES = [
        ('', ' '),
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
    ]

    subject = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)
    note = models.TextField()
    related_to = models.CharField(max_length=255, choices=RELATED_TO_CHOICES, blank=True)

    def __str__(self):
        return self.subject

    
'''
class createInvoices(models.Model):
 
    title = models.CharField(max_length=255)
    customer_name = models.CharField(max_length=255)
    due_date = models.DateField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)


    invoice_number = models.CharField(max_length=100, blank=True)
    quotation_number = models.CharField(max_length=100, blank=True)
    invoice_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=[('Open', 'Open'), ('Closed', 'Closed'), ('Pending', 'Pending')], default='Open')

    account = models.CharField(max_length=255, blank=True)
    contact = models.CharField(max_length=255, blank=True)
    billing_address = models.TextField(blank=True)
    shipping_address = models.TextField(blank=True)


    currency = models.CharField(max_length=10, choices=[('USD', 'USD'), ('EUR', 'EUR'), ('GBP', 'GBP')], default='USD')
    line_items = models.TextField(blank=True)  # For simplicity, you can use JSON or a dedicated model for line items

  
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.title'''



class agentProjects(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    draft = models.BooleanField(default=False)
    start_date = models.DateField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    end_date = models.DateField()
    consider_working_days = models.BooleanField(default=False)
    project_manager = models.CharField(max_length=100)
    project_template = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class AgentTemplate(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('in_review', 'In Review'),
        ('underway', 'Underway'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
]

    PRIORITY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]

    template_name = models.CharField(max_length=255)
    consider_working_days = models.BooleanField(default=False)
    project_manager = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.template_name



# class createInvoice(models.Model):
#     title = models.CharField(max_length=255)
#     customer_name = models.CharField(max_length=255)
#     due_date = models.DateField()
#     assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     description = models.TextField(blank=True, null=True)
    
#     invoice_number = models.CharField(max_length=100, blank=True, null=True)
#     quotation_number = models.CharField(max_length=100, blank=True, null=True)
#     invoice_date = models.DateField(blank=True, null=True)
#     status = models.CharField(max_length=50, choices=[('open', 'Open'), ('closed', 'Closed'), ('pending', 'Pending')], default='open')
    
#     account = models.CharField(max_length=255)
#     contact = models.CharField(max_length=255)
#     billing_address = models.TextField(blank=True, null=True)
#     shipping_address = models.TextField(blank=True, null=True)
    
#     currency = models.CharField(max_length=10, default='USD')
#     line_items = models.TextField(blank=True, null=True)
    
#     total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     shipping = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     adjustment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
#     grand_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

#     def __str__(self):
#         return self.title


# class ComposedEmail(models.Model):
#     """Model to store composed email details."""
#     template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True)
#     related_to = models.CharField(max_length=255, blank=True, null=True)
#     from_address = models.EmailField()
#     to_address = models.EmailField()
#     cc_address = models.TextField(blank=True, null=True)  # Can store multiple emails separated by commas
#     bcc_address = models.TextField(blank=True, null=True)  # Can store multiple emails separated by commas
#     subject = models.CharField(max_length=255)
#     body = models.TextField()
#     send_plain_text = models.BooleanField(default=False)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):

#         return f"Email to {self.to_address} - Subject: {self.subject[:50]}"


# from django.db import models
# from django.contrib.auth.models import User

# class Invoice(models.Model):
#     # Title of the invoice
#     title = models.CharField(max_length=255)

#     # Unique invoice number
#     invoice_number = models.CharField(max_length=255, unique=True)

#     # Quote number (can be linked to a quote)
#     quote_number = models.CharField(max_length=255)

#     # Date when the invoice was created
#     invoice_date = models.DateField()

#     # Due date for the payment
#     due_date = models.DateField()

#     # The person to whom the invoice is assigned
#     assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

#     # Status of the invoice (Draft, Sent, Paid)
#     STATUS_CHOICES = [
#         ('Draft', 'Draft'),
#         ('Sent', 'Sent'),
#         ('Paid', 'Paid'),
#     ]
#     status = models.CharField(max_length=50, choices=STATUS_CHOICES)

#     def __str__(self):
#         return f"Invoice {self.invoice_number} - {self.title}"

#         return f"Email to {self.to_address} - Subject: {self.subject[:50]}"
