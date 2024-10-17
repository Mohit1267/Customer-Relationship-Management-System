from django.db import models
from users.models import RegisterUser
from django.conf import settings





class CallingAgent(models.Model):
    calling_agent_id = models.AutoField(primary_key=True)
    calling_agent_name = models.CharField(max_length=50)
    calling_agent_email = models.EmailField(max_length=50)
    calling_agent_contact = models.CharField(max_length=15)

    class Meta:
        managed = False  # Prevent Django from managing the table (no migrations)
        db_table = 'CallingAgent' 
    def __str__(self):
        return f"{self.calling_agent_id}"

#have to change this database 

# Create your models here.

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
    status = models.CharField(max_length=4, choices=LEAD_STATUS_CHOICES, default='COLD')
    created_by = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, related_name='leads_by',default=11)
    remarks = models.TextField( default="nothing" )
    nextdate = models.DateField(default="2024-11-11")
    
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
    contact = models.CharField(max_length= 50)
    billing_address = models.TextField()
    shipping_address = models.TextField()

    total = models.CharField(max_length=50)
    discount = models.CharField(max_length=50)
    sub_total = models.CharField(max_length=50)
    shipping = models.CharField(max_length=50)
    shipping_tax = models.CharField(max_length=50)
    tax = models.CharField(max_length=50)
    grandtotal = models.CharField(max_length=50)
    date = models.DateField(default="2000-10-10")
    assigned_to = models.ForeignKey(RegisterUser, on_delete= models.CASCADE, default=1)


from django.db import models

class Account(models.Model):
    # Basic Fields
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    email_address = models.EmailField()
    
    # Billing Information
    billing_address = models.CharField(max_length=255)
    billing_street = models.CharField(max_length=255)
    billing_postal_code = models.CharField(max_length=20)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100)
    billing_country = models.CharField(max_length=100)
    
    # Description
    description = models.TextField(blank=True, null=True)
    
    # Assigned To
    assigned_to = models.CharField(max_length=100, blank=True, null=True)
    
    # Shipping Information
    shipping_address = models.CharField(max_length=255, blank=True, null=True)
    shipping_street = models.CharField(max_length=255, blank=True, null=True)
    shipping_postal_code = models.CharField(max_length=20, blank=True, null=True)
    shipping_city = models.CharField(max_length=100, blank=True, null=True)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_country = models.CharField(max_length=100, blank=True, null=True)
    
    # Account Detail
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

from django.db import models
from django.core.validators import RegexValidator

password_regex = RegexValidator(
    regex=r'^(?=.[A-Z])(?=.[a-z])(?=.\d)(?=.[@$!%?&])[A-Za-z\d@$!%?&]{8,}$',
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


class Document(models.Model):
    FILE_TYPES = (
        ('pdf', 'PDF'),
        ('doc', 'Word Document'),
        ('xls', 'Excel Spreadsheet'),
        # Add other file types here
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
        # Add other categories here
    )
    
    SUBCATEGORIES = (
        ('subcat1', 'Subcategory 1'),
        ('subcat2', 'Subcategory 2'),
        # Add other subcategories here
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
    assigned_to = models.ForeignKey(RegisterUser, on_delete=models.SET_NULL, null=True)  # Assuming User model for assignee

    def __str__(self):
        return self.document_name


