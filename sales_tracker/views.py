# from typing import Any
# from django.db.models.query import QuerySet
import json
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Count, OuterRef, Subquery
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from typing import Any
from django.db import connection
from django.db.models import Count
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
# import pymysql
from django.contrib.auth import get_user_model
from users.models import Profile, RegisterUser, Location
from .models import MiningData, ContactData, LeadsData, OpportunityData, QuotesData , CallingAgent,Schedule_Meeting, Schedule_Calling
from .forms import MiningForm, ContactForm, LeadForm, OpportunityForm, QuoteForm, agentmeeting, DocumentForm, TaskForm,agentcalling, NoteForm, InvoiceForm
from .analysis import generate_bar_chart, TotalDays,generate_bar_chart2
from .admin_analysis import Att_perct,Late_perct ,Mining_Count ,Leads_Count,EachMinerTarget,Time_worked,Productivity,admin_attendance_graph, dailymining, monthlymining, quarterlymining,yearlymining, yearlyleads,quarterlyleads,monthlyleads,dailyleads
from .requirements import timer
from django.http import HttpResponseForbidden
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import AttendanceRecord
import random
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from .forms import agentmeeting
from django.http import JsonResponse
from datetime import date


def get_timer_value(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    return JsonResponse({
        'hrs': int(elapsed_time[0]),
        'min': int(elapsed_time[1]),
        'sec': int(elapsed_time[2])
    })



def Dashboards(request):
    if (request.user.profile.branch == 'admin'):
        context = {}
        attendances = AttendanceRecord.objects.all()
        att = Att_perct()
        late = Late_perct()
        attendence_graph = admin_attendance_graph(request)
        context['admin_message'] = "Welcome to the Admin Page"
        context['attendances'] = attendances
        context['attendence_graph'] = attendence_graph
        context['att'] = att
        context['temp'] = "temp"
        # context['request'] = request
        latitude = request.session.get('latitude')
        longitude = request.session.get('longitude')
        context['lat'] = latitude
        context['long'] = longitude
        
        # context['late'] = Late_perct
        context['late'] = late
        return render(request,'sales_tracker/admin.html',context)
    elif(request.user.profile.branch == 'miner'):
        context = {}
        user = request.user
        context["user"] = user.username
        utc_login_time = user.last_login
        elapsed_time = timer(utc_login_time)
        context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        users = request.user
        u = RegisterUser.objects.get(email=users)
        u = u.id
        today_mining = MiningData.objects.filter(date = now_date,created_by=u)
        today_mining_count = today_mining.count()
        context["mining_count"] = today_mining_count
        today_lead = LeadsData.objects.filter(date = now_date)
        today_lead_count = today_lead.count()
        context["lead_count"] = today_lead_count
        today_contact = ContactData.objects.filter(date = now_date)
        today_contact_count = today_contact.count()
        context["contact_count"] = today_contact_count
        today_Opportunity = OpportunityData.objects.filter(date = now_date)
        today_Opportunity_count = today_Opportunity.count()
        context["Opportunity_count"] = today_Opportunity_count
        graph_html = dailymining(request)
        context["graph_html"] = graph_html
        monthg = monthlymining(request)
        context["monthlymining"] = monthg
        quater = quarterlymining(request)
        context["quarterlymining"] = quater
        yearly = yearlymining(request)
        context["yearlymining"] = yearly

        return render(request,'sales_tracker/index.html',context)
    elif request.user.profile.branch == 'agent':
        context = {}
        if request.method == 'POST':
            data = json.loads(request.body)  # Load the JSON data
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            request.session['latitude'] = latitude
            request.session['longitude'] = longitude
            context = {
            "lat": latitude,
            "long": longitude,
            }
        else:
            latitude = request.session.get('latitude')
            longitude = request.session.get('longitude')
        
        context = {
            "lat": latitude,
            "long": longitude,
            "user": RegisterUser.objects.get(email=request.user.email),
        }
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        context["Tocall"] = MiningData.objects.filter(assigned_to=context["user"].id, date=now_date)
        context["daily"] = dailyleads(request)
        context["monthly"] = monthlyleads(request)
        context["quarterly"] = quarterlyleads(request)
        context["yearlyl"] = yearlyleads(request)
        return render(request, 'sales_tracker/agent.html', context)
    elif(request.user.profile.branch == 'sales'):
        context = {}
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        users = request.user
        u = RegisterUser.objects.get(email=users)
        u = u.id
        HLeads = LeadsData.objects.filter(assigned_to=u,date = now_date, status = "HOT")
        CLeads = LeadsData.objects.filter(assigned_to=u,date = now_date, status = "COLD")
        MLeads = LeadsData.objects.filter(assigned_to=u,date = now_date, status = "MILD")
        context["user"] = u
        context["HLeads"] = HLeads
        context["CLeads"] = CLeads
        context["MLeads"] = MLeads
        # print(ToCall, "This is the value of ToCall")
        return render(request,'sales_tracker/sales.html',context)



def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.profile.branch == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to view this page.")
    return _wrapped_view

def miner_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.profile.branch == 'miner':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to view this page.")
    return _wrapped_view

def agent_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.profile.branch == 'agent':
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to view this page.")
    return _wrapped_view

def assign_miningCt():
    # Get the user with the least assignments
    least_occurring_assigned_to_id = (
        MiningData.objects
        .filter(assigned_to__profile__branch='agent')
        .values('assigned_to')
        .annotate(count=Count('assigned_to'))
        .order_by('count')
        .first()
    )

    # If there are no records yet, assign randomly to one of the agents
    if not least_occurring_assigned_to_id:
        # Get all users with the 'agent' branch
        agent_users = RegisterUser.objects.filter(profile__branch='agent')
        if agent_users.exists():
            # Randomly select one agent
            return random.choice(agent_users)
        else:
            # Handle case where there are no agents
            raise ObjectDoesNotExist("No agents found to assign.")

    # Otherwise, assign to the least occurring agent
    assigned_to_id = least_occurring_assigned_to_id['assigned_to']
    return RegisterUser.objects.get(id=assigned_to_id)


import re
import datetime  # Ensure datetime is imported
from django.shortcuts import render, redirect


def mining_view(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs": int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    today_mining = MiningData.objects.filter(date=now_date)
    today_mining_count = today_mining.count()

    if request.method == "POST":
        form = MiningForm(request.POST)
        state = request.POST.get("state")
        city = request.POST.get("city")
        zone = request.POST.get("zone")

        organisation_name = form.data.get("organisation_name")
        customer_first_name = form.data.get("customer_first_name")
        customer_last_name = form.data.get("customer_last_name")
        customer_contact_number = form.data.get("customer_contact_number")
        customer_mobile_number = form.data.get("customer_mobile_number")
        company_revenue = form.data.get("company_revenue")
        customer_offering = form.data.get("customer_offering")
        competition_of_AT = form.data.get("competition_of_AT")
        stock_market_registered = form.data.get("stock_market_registered")
        it_spending_budget = form.data.get("IT_spending_budget")
        source_of_data_mining = form.data.get("source_of_data_mining")
        company_emp_size = form.data.get("company_emp_size")

        # Validate organisation_name (allow only alphabets and numbers)
        if not re.match("^[A-Za-z0-9 ]+$", organisation_name):
            form.add_error('organisation_name', "Organisation name can only contain alphabets and numbers.")
            return render(request, "sales_tracker/mining.html", {
                "form": form,
                "timer": formated_timer,
                "mining_count": today_mining_count
            })

        # Validate customer_first_name (allow only alphabets)
        if not re.match("^[A-Za-z ]+$", customer_first_name):
            form.add_error('customer_first_name', "First name can only contain alphabets.")
            return render(request, "sales_tracker/mining.html", {
                "form": form,
                "timer": formated_timer,
                "mining_count": today_mining_count
            })

        # Validate customer_last_name (allow only alphabets)
        if not re.match("^[A-Za-z ]+$", customer_last_name):
            form.add_error('customer_last_name', "Last name can only contain alphabets.")
            return render(request, "sales_tracker/mining.html", {
                "form": form,
                "timer": formated_timer,
                "mining_count": today_mining_count
            })

        # Validate customer_contact_number (must be exactly 10 digits)
        if not re.match(r"^\d{10}$", customer_contact_number):
            form.add_error('customer_contact_number', "Contact number must be exactly 10 digits.")
            return render(request, "sales_tracker/mining.html", {
                "form": form,
                "timer": formated_timer,
                "mining_count": today_mining_count
            })

        # Validate customer_mobile_number (must be exactly 10 digits)
        if not re.match(r"^\d{10}$", customer_mobile_number):
            form.add_error('customer_mobile_number', "Mobile number must be exactly 10 digits.")
            return render(request, "sales_tracker/mining.html", {
                "form": form,
                "timer": formated_timer,
                "mining_count": today_mining_count
            })

        # Validate company_revenue (must be a number)
        if not company_revenue.isdigit():
            form.add_error('company_revenue', "Company revenue must be a numeric value.")
            return render(request, "sales_tracker/mining.html", {
                "form": form,
                "timer": formated_timer,
                "mining_count": today_mining_count
            })

        # Validate customer_offering (allow only alphabets and numbers)
        if not re.match("^[A-Za-z0-9 ]+$", customer_offering):
            form.add_error('customer_offering', "Customer offering can only contain alphabets and numbers.")
            return render(request, "sales_tracker/mining.html", {
                "form": form,
                "timer": formated_timer,
                "mining_count": today_mining_count
            })

        # Validate competition_of_AT (allow only alphabets and numbers)
        if not re.match("^[A-Za-z0-9 ]+$", competition_of_AT):
            form.add_error('competition_of_AT', "Competition of AT can only contain alphabets and numbers.")
            return render(request, "sales_tracker/mining.html", {
                "form": form,
                "timer": formated_timer,
                "mining_count": today_mining_count
            })

        # Validate stock_market_registered (allow only alphabets and numbers)
        if not re.match("^[A-Za-z0-9 ]+$", stock_market_registered):
            form.add_error('stock_market_registered', "Stock market registered can only contain alphabets and numbers.")
            return render(request, "sales_tracker/mining.html", {
                "form": form,
                "timer": formated_timer,
                "mining_count": today_mining_count
            })

        # Validate IT spending budget (must be a number)
        if not it_spending_budget.isdigit():
            form.add_error('IT_spending_budget', "IT spending budget must be a numeric value.")
            return render(request, "sales_tracker/mining.html", {
                "form": form,
                "timer": formated_timer,
                "mining_count": today_mining_count
            })

        # Validate source_of_data_mining (allow only alphabets and numbers)
        if not re.match("^[A-Za-z0-9 ]+$", source_of_data_mining):
            form.add_error('source_of_data_mining', "Source of data mining can only contain alphabets and numbers.")
            return render(request, "sales_tracker/mining.html", {
                "form": form,
                "timer": formated_timer,
                "mining_count": today_mining_count
            })

        # Validate company_emp_size (must be a positive number)
        if not company_emp_size.isdigit() or int(company_emp_size) <= 0:
            form.add_error('company_emp_size', "Employee size must be a positive numeric value.")
            return render(request, "sales_tracker/mining.html", {
                "form": form,
                "timer": formated_timer,
                "mining_count": today_mining_count
            })

        try:
            MiningData.objects.get(organisation_name=organisation_name)
            print("hello world")
        except MiningData.DoesNotExist:
            assignTo = assign_miningCt()
            now_date_time = datetime.datetime.now()
            now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
            username = request.user.username
            mining_details = MiningData(
                organisation_name=organisation_name,
                customer_first_name=customer_first_name,
                customer_last_name=customer_last_name,
                customer_address=form.data.get("customer_address"),
                customer_contact_number=customer_contact_number,
                customer_mobile_number=customer_mobile_number,
                customer_email=form.data.get("customer_email"),
                company_revenue=company_revenue,
                company_emp_size=company_emp_size,
                customer_offering=customer_offering,
                competition_of_AT=competition_of_AT,
                stock_market_registered=stock_market_registered,
                influncer=form.data.get("influncer") == "on",
                desition_maker=form.data.get("desition_maker") == "on",
                IT_spending_budget=it_spending_budget,
                source_of_data_mining=source_of_data_mining,
                date=now_date,
                assigned_to=assignTo,
                created_by=user,
                state=state,
                city=city,
                region=zone,
            )
            mining_details.save()
            print("Hello world 4")
            return redirect("mining")

        print("Hello world 2")
        return render(request, "sales_tracker/mining.html", {
            "form": form,
            "timer": formated_timer,
            "mining_count": today_mining_count
        })

    else:
        form = MiningForm()

    return render(request, "sales_tracker/mining.html", {
        "form": form,
        "timer": formated_timer,
        "mining_count": today_mining_count
    })




# class DataView(ListView):
#     template_name = "sales_tracker/data.html"
#     model = MiningData
#     context_object_name = "mined_data"

#     def get_queryset(self):
#         base_query =  super().get_queryset()
#         now_date_time = datetime.datetime.now()
#         now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
#         data = base_query.filter(date = f"{now_date}")
#         return data
    
#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         request = self.request
#         user = request.user
#         utc_login_time = user.last_login
#         elapsed_time = timer(utc_login_time)
#         context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
#         now_date_time = datetime.datetime.now()
#         now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
#         today_mining = MiningData.objects.filter(date = now_date)
#         today_mining_count = today_mining.count()
#         context["mining_count"] = today_mining_count
#         return context
    
class DetailDataView(DetailView):
    template_name = "sales_tracker/detail.html"
    model = MiningData
    context_object_name = "detail"  

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        utc_login_time = user.last_login
        elapsed_time = timer(utc_login_time)
        context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        today_mining = MiningData.objects.filter(date = now_date)
        today_mining_count = today_mining.count()
        context["mining_count"] = today_mining_count
        return context

class CallView(TemplateView):
    template_name = "sales_tracker/call.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        utc_login_time = user.last_login
        elapsed_time = timer(utc_login_time)
        context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        today_mining = MiningData.objects.filter(date = now_date)
        today_mining_count = today_mining.count()
        context["mining_count"] = today_mining_count
        return context

class VideoCallView(TemplateView):
    template_name = "sales_tracker/videocall.html"


from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required
@csrf_exempt
def join_meet(request):
    if request.method == "POST":
        room_id = request.POST["id"]
        return redirect(f'/videocall?roomID={room_id}')
    return render(request, "sales_tracker/join.html")


class Agent(TemplateView):
    template_name = "sales_tracker/agent.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        users = request.user
        u = RegisterUser.objects.get(email=users)
        u = u.id
        ToCall = MiningData.objects.filter(assigned_to=u)
        context["user"] = u
        context["Tocall"] = ToCall
        return context
# class ContactCreateView(CreateView):
#     model = ContactData
#     form_class = ContactForm
#     template_name = "sales_tracker/create_contact.html"
#     success_url = "message"
    
    
class Message(TemplateView):
    template_name = "sales_tracker/message.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["message"] = "data stored successfully"
        return context
    
class Agentmessage(TemplateView):
    template_name = "sales_tracker/agentmessage.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["message"] = "data stored successfully"
        return context

# class LeadCreateView(CreateView):
#     model = LeadsData
#     form_class = LeadForm
#     template_name = "sales_tracker/create_contact.html"
#     success_url = "message"
    

# def assign_contact_to_agent():
#     # Get all agents who are active and can accept contacts
#     agents = Profile.objects.filter(branch='agent', can_login=True)

#     # Find the agent with the least assigned contacts   
#     agent = agents.annotate(num_contacts=Count('user_id')).order_by('num_contacts').first()
#     print(agent,"this is agent ")

#     return agent




def Create_contact_view(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    today_mining = MiningData.objects.filter(date = now_date)
    today_mining_count = today_mining.count()
    if request.method == "POST":
        form = ContactForm(request.POST)
        try:
            ContactData.objects.get(email_id = form.data.get("email_id"))
        except:
            # assigned_agent = assign_contact_to_agent()
            now_date_time = datetime.datetime.now()
            now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
            username = request.user.username
            # claid = request.POST.get("calling_agent")
            contact_details = ContactData(
                first_name = form.data.get("first_name"),
                last_name = form.data.get("last_name"),
                email_id = form.data.get("email_id"),
                contact_number = form.data.get("contact_number"),
                job_title = form.data.get("job_title"),
                address = form.data.get("address"),
                organization = MiningData.objects.get(organisation_name = form.data.get("organization")),
                date = now_date,
                # assigned_to=assigned_agent.user,
                
                # assigned_to = get_user_model().objects.get(username=username),
                # calling_agent = CallingAgent.objects.get(calling_agent_id=claid),
            )
                # calling_agent=CallingAgent.objects.get(id=form.calling_agent.get("calling_agent"))
            contact_details.save()

            return redirect("create_contact")
        
        return render(request, "sales_tracker/create_contact.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count,"calling_agents": CallingAgent.objects.all()})


    else:
        form = ContactForm()
    return render(request, "sales_tracker/create_contact.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count,"calling_agents": CallingAgent.objects.all()})




def assign_leadCt():
    # Get the user with the least assignments
    least_occurring_assigned_to_id = (
        LeadsData.objects
        .filter(assigned_to__profile__branch='sales')
        .values('assigned_to')
        .annotate(count=Count('assigned_to'))
        .order_by('count')
        .first()
    )

    # If there are no records yet, assign randomly to one of the sales agents
    if not least_occurring_assigned_to_id:
        # Get all users with the 'sales' branch
        sales_users = RegisterUser.objects.filter(profile__branch='sales')
        if sales_users.exists():
            # Randomly select one sales agent
            return random.choice(sales_users)
        else:
            # Handle case where there are no sales agents
            raise ObjectDoesNotExist("No sales agents found to assign.")

    # Otherwise, assign to the least occurring sales agent
    assigned_to_id = least_occurring_assigned_to_id['assigned_to']
    return RegisterUser.objects.get(id=assigned_to_id)


def Create_lead_view(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    today_mining = MiningData.objects.filter(date = now_date)
    today_mining_count = today_mining.count()
    if request.method == "POST":
        form = LeadForm(request.POST)
        try:
            LeadsData.objects.get(contact_link = ContactData.objects.get(pk = form.data.get("contact_link")))
        except:
            assign_lead = assign_leadCt()
            now_date_time = datetime.datetime.now()
            now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
            username = request.user.username
            contact_details = LeadsData(
                lead_name = form.data.get("lead_name"),
                first_name = form.data.get("first_name"),
                last_name = form.data.get("last_name"),
                email_id = form.data.get("email_id"),
                contact_number = form.data.get("contact_number"),
                job_title = form.data.get("job_title"),
                address = form.data.get("address"),
                contact_link = ContactData.objects.get(pk = form.data.get("contact_link")),
                date = now_date,
                # assigned_to = get_user_model().objects.get(username=username),
                assigned_to = assign_lead,
                created_by = user,
                nextdate = form.data.get("nextdate"),
                remarks = form.data.get("remarks")
            )
            print("hello bhai")
            contact_details.save()

            return redirect("create_lead")
        
        return render(request, "sales_tracker/create_lead.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


    else:
        form = LeadForm()
    return render(request, "sales_tracker/create_lead.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


def Create_opportunity_view(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    today_mining = MiningData.objects.filter(date = now_date)
    today_mining_count = today_mining.count()
    if request.method == "POST":
        form = OpportunityForm(request.POST)
        
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        username = request.user.username
        contact_details = OpportunityData(
            opportunity_name = form.data.get("opportunity_name"),
            amount = form.data.get("amount"),
            sales_stage = form.data.get("sales_stage"),
            probability = form.data.get("probability"),
            next_step = form.data.get("next_step"),
            description = form.data.get("description"),
            expected_close_date = form.data.get("expected_close_date"),
            lead_source = form.data.get("lead_source"),
            lead = LeadsData.objects.get(pk = form.data.get("lead")),
            date = now_date,
            assigned_to = get_user_model().objects.get(username=username)

        )
        contact_details.save()

        return redirect("message")
        
        # return render(request, "sales_tracker/create_lead.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


    else:
        form = OpportunityForm()
    return render(request, "sales_tracker/create_opportunity.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})

def Create_quote_view(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    today_mining = MiningData.objects.filter(date = now_date)
    today_mining_count = today_mining.count()
    if request.method == "POST":
        form = QuoteForm(request.POST)
        
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        username = request.user.username
        quote_details = QuotesData(
            title = form.data.get("title"),
            valid_until = form.data.get("valid_until"),
            approval_status = form.data.get("approval_status"),
            opportunity = OpportunityData.objects.get(pk = form.data.get("opportunity")),
            quote_stage = form.data.get("quote_stage"),
            invoice_status = form.data.get("invoice_status"),
            approval_issues_description = None if form.data.get("approval_issues_description") == "" else form.data.get("approval_issues_description"),
            lead_source = form.data.get("lead_source"),
            account = form.data.get("account"),
            contact = form.data.get("contact"),
            billing_address = form.data.get("billing_address"),
            shipping_address = form.data.get("shipping_address"),
            total = form.data.get("total"),
            discount = form.data.get("discount"),
            sub_total = form.data.get("sub_total"),
            shipping = form.data.get("shipping"),
            shipping_tax = form.data.get("shipping_tax"),
            tax = form.data.get("tax"),
            grandtotal = form.data.get("grandtotal"),
            date = now_date,
            assigned_to = get_user_model().objects.get(username=username)

        )
        quote_details.save()

        return redirect("message")
        
        # return render(request, "sales_tracker/create_lead.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


    else:
        form = QuoteForm()
    return render(request, "sales_tracker/create_quote.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})



from django.views import View
from .forms import SortForm

class MiningsView(View):
    def get(self, request):
        form = SortForm()
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
        datas = MiningData.objects.filter(date = now_date)
        return render(request, "sales_tracker/view_data.html", {"form":form, "datas": datas})
    def post(self, request):
        form = SortForm(request.POST)
        time = form.data.get("select")
        if time == "week":
            from datetime import date, timedelta
            today = date.today()
            days_ago = today - timedelta(days=7)
            datas = MiningData.objects.filter(date__lte = today, date__gte = days_ago )
        elif time == "month":
            from datetime import date, timedelta
            today = date.today()
            days_ago = today - timedelta(days=30)
            
            datas = MiningData.objects.filter(date__lte = today, date__gte = days_ago )
        elif time == "day":
            from datetime import date, timedelta
            today = date.today()
            datas = MiningData.objects.filter(date = today)
        return render(request, "sales_tracker/view_data.html", {"form":form, "datas": datas})
    





# class LeadView(ListView):
#     template_name = "sales_tracker/data2.html"
#     model = LeadsData
#     context_object_name = "lead_data"

#     def get_queryset(self):
#         base_query =  super().get_queryset()
#         now_date_time = datetime.datetime.now()
#         now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
#         data = base_query.filter(date = f"{now_date}")
#         return data

#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         request = self.request
#         user = request.user
#         utc_login_time = user.last_login
#         elapsed_time = timer(utc_login_time)
#         context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
#         now_date_time = datetime.datetime.now()
#         now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
#         todays_lead = LeadsData.objects.filter(date = now_date)
#         today_lead_count = todays_lead.count()
#         context["lead_count"] = today_lead_count
#         return context
    

class BaseListView(ListView):
    template_name = "sales_tracker/data.html"
    model = None
    context_object_name = "data_list"
    context_count_name = None

    def get_queryset(self):
        base_query = super().get_queryset()
        time_frame = self.request.GET.get('time_frame', 'today')  # Get the time frame from GET parameters
        now_date_time = datetime.datetime.now()
        state = self.request.GET.get('state', None)
        zone = self.request.GET.get('zone', None)

        if time_frame == "weekly":
            start_date = now_date_time - datetime.timedelta(days=now_date_time.weekday())  # Start of the week
            end_date = start_date + datetime.timedelta(days=7)  # End of the week
            base_query = base_query.filter(date__range=[start_date.date(), end_date.date()])
        elif time_frame == "monthly":
            start_date = now_date_time.replace(day=1)  # Start of the month
            end_date = (start_date + datetime.timedelta(days=31)).replace(day=1)  # Start of next month
            base_query = base_query.filter(date__range=[start_date.date(), end_date.date()])
            base_query.filter(date__range=[start_date.date(), end_date.date()])
        elif time_frame == "quarterly":
            quarter = (now_date_time.month - 1) // 3 + 1
            start_date = datetime.datetime(now_date_time.year, (quarter - 1) * 3 + 1, 1)
            end_date = (start_date + datetime.timedelta(days=92)).replace(day=1)  # Roughly add 3 months
            base_query = base_query.filter(date__range=[start_date.date(), end_date.date()])
        elif time_frame == "yearly":
            start_date = datetime.datetime(now_date_time.year, 1, 1)  # Start of the year
            end_date = datetime.datetime(now_date_time.year + 1, 1, 1)  # Start of next year
            base_query = base_query.filter(date__range=[start_date.date(), end_date.date()])
        else:  # Default to today
            today = now_date_time.date()
            base_query = base_query.filter(date=today)
        if state and state != 'all':
            base_query = base_query.filter(state=state)
        if zone and zone != 'all':
            base_query = base_query.filter(region=zone)
        return base_query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        utc_login_time = user.last_login
        elapsed_time = timer(utc_login_time)
        context["timer"] = {"hrs": int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
        
        # Count today's leads
        now_date_time = datetime.datetime.now()
        today = now_date_time.date()
        todays_lead = LeadsData.objects.filter(date=today)
        today_lead_count = todays_lead.count()
        context[self.context_count_name] = today_lead_count
        context['time_frame'] = self.request.GET.get('time_frame', 'today')
        return context

class DataView(BaseListView):
    template_name = "sales_tracker/data.html"
    model = MiningData
    context_count_name = 'mining_count'   

class LeadView(BaseListView):
    template_name = "sales_tracker/leadsdata.html"
    model = LeadsData
    count_context_name = 'lead_count'

class OpportunityView(BaseListView):
    template_name = "sales_tracker/opp_data.html"
    model = OpportunityData
    count_context_name = 'opportunity_count'
class QuotesView(BaseListView):
    
    template_name = "sales_tracker/quotesdata.html"
    model = QuotesData
    count_context_name = 'opportunity_count'

# class DSRview(BaseListView):
#     template_name = "sales_tracker/agentDsrdata.html"
#     model = DsrData
#     count_context_name = 'agentDsr_count'









# def Tocall(request):
#     context = {}
#     user = request.user
#     utc_login_time = user.last_login
#     elapsed_time = timer(utc_login_time)
#     formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
#     now_date_time = datetime.datetime.now()
#     now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}" 
#     orgs = ContactData.objects.filter(date=now_date) 
#     orgs_list = [orgsN.organization for orgsN in orgs]
#     context['orgs_list'] = orgs_list
#     context['timer'] = formated_timer

#     return render(request, "sales_tracker/data2.html", context)


class Tocall(TemplateView):
    template_name = "sales_tracker/data2.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        request = self.request
        user = request.user
        utc_login_time = user.last_login
        elapsed_time = timer(utc_login_time)
        context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
        now_date_time = datetime.datetime.now()
        now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}" 
        orgs = ContactData.objects.filter(date=now_date) 
        orgs_list = [orgsN.organization for orgsN in orgs]
        context['orgs_list'] = orgs_list
        return context



def Tocall_detail(request, pk):
    context = {}
    context['pk'] = pk
    user = request.user
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    print("hwllo")
    mining_data = get_object_or_404(MiningData, organisation_name=pk)
    # Retrieve the related ContactData entries

    contact_data_list = ContactData.objects.filter(organization=mining_data,date=now_date)
    
    # Prepare the data to be sent to the template       
    context = {
        'mining_data': mining_data,
        'contact_data_list': contact_data_list
    }
    # contact = ContactData.objects.get(organization=pk)
    # context['contact'] = contact
    return render(request, "sales_tracker/Detailtocall.html", context)

def DetailCalling(request, pk):
    context = {}
    context['pk'] = pk
    mining_data = get_object_or_404(MiningData, organisation_name=pk)
    context = {
        'mining_data': mining_data
    }

    return render(request,"sales_tracker/detailcalling.html",context)

    pass

def DetailSales(request, pk):
    context = {}
    context['pk'] = pk
    leads_data = get_object_or_404(LeadsData, lead_name=pk)
    context = {
        'leads_data': leads_data
    }

    return render(request,"sales_tracker/detail_leads_sales.html",context)


def get_calling_agents(request):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM CallingAgent")
        rows = cursor.fetchall()
        
        # Optionally, you can format the data as needed
        data = [
            {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'contact': row[3],
                'call_date': row[4]
            }
            for row in rows
        ]
        context['data'] = data
        return render(request, "sales_tracker/call_center.html",context)
  



def Attendence(request):    
    # generate_bar_chart()
    context = {}
    user = request.user
    days = TotalDays(request)
    u = RegisterUser.objects.get(email=user)
    context['u'] = u.username
    context['days'] = days
    return render(request, "sales_tracker/MinerAttendence.html",context)


def attendance_list(request):
    attendances = AttendanceRecord.objects.all()
    return render(request, "sales_tracker/ADMIN.html", {'attendances': attendances})


@method_decorator(admin_required, name = 'dispatch')
class Admin_reports(TemplateView):
    template_name = "sales_tracker/reports.html"
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)

        return context

@method_decorator(admin_required, name = 'dispatch')
class MinerActivity(TemplateView):
    template_name = "sales_tracker/MinerActivity.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Mining_Count()
        Miner = Profile.objects.filter(branch = "miner")
        MinerC = Profile.objects.filter(branch = "miner").count()
        Total_Mining = MiningData.objects.count()
        Exp_Mining =   AttendanceRecord.objects.values('date').distinct().count()
        context['Miner'] = Miner
        context['Total_Mining'] = Total_Mining
        context['Exp_Mining'] = Exp_Mining*MinerC*40
        # context['MinerC'] = MinerC
        return context

@method_decorator(admin_required, name = 'dispatch')
class LeadsActivity(TemplateView):
    template_name = "sales_tracker/LeadsActivity.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Leads_Count()
        Agents = Profile.objects.filter(branch = "agent")
        AgentsC = Profile.objects.filter(branch = "agent").count()
        Total_Leads = LeadsData.objects.count()
        Exp_Leads =   AttendanceRecord.objects.values('date').distinct().count()
        context['Agents'] = Agents
        context['Total_Leads'] = Total_Leads
        context['Exp_Leads'] = Exp_Leads*AgentsC*4
        # context['MinerC'] = MinerC
        return context
    
@method_decorator(admin_required, name = 'dispatch')
class EmployeeDetail(TemplateView): 
    template_name = "sales_tracker/employee_detail.html"
    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        request = self.request
        users = request.user
        pk = self.kwargs.get('pk')
        u = RegisterUser.objects.get(email=users)
        u = u.id
        generate_bar_chart2(pk)
        Miner_Details = EachMinerTarget(pk)
        context["Miner_Details"] = Miner_Details
        return context
    

# @admin_required
@method_decorator(admin_required, name = 'dispatch')
class AdminAnalysis(TemplateView):
    template_name = "sales_tracker/admin_analysis.html"
    def get_context_data(self, **kwargs: Any):
        request = self.request
        context = super().get_context_data(**kwargs)
        time_graph = Time_worked(request)
        graph_html = Productivity(request)
        context['graph_html']=graph_html
        context['time_graph']=time_graph
        return context


import json
class maps(View):
    template_name = "sales_tracker/maps.html"

    def get(self, request):
        context = {}
        latitude = request.session.get('latitude')
        longitude = request.session.get('longitude')
        context['lat'] = latitude
        context['long'] = longitude
        return render(request, self.template_name, context)

    def post(self, request):
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Save latitude and longitude to session
        request.session['latitude'] = latitude
        request.session['longitude'] = longitude

        # Save to the database
        profile = Profile.objects.get(user=request.user)
        now = timezone.now()
        today = now.date()

        # Fetch the last location entry for the profile
        last_location = Location.objects.filter(profile=profile).order_by('-date', '-time').first()

        # Define a time threshold for significant time difference (e.g., 5 minutes)
        time_threshold = timedelta(minutes=5)

        # Create a new entry if the location is different or the date is different
        if not last_location or (last_location.latitude != latitude or last_location.longitude != longitude) or (now - datetime.combine(last_location.date, last_location.time) > time_threshold):
            Location.objects.create(profile=profile, latitude=latitude, longitude=longitude, date=today, time=now.time())

        return JsonResponse({'status': 'success'})

def ViewQuote(request):
    pass



import re
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import ContactData, MiningData, CallingAgent
import datetime

def Agentcontact(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs": int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"

    if request.method == "POST":
        form = ContactForm(request.POST)
        
        first_name = form.data.get("first_name")
        last_name = form.data.get("last_name")
        email_id = form.data.get("email_id")
        contact_number = form.data.get("contact_number")
        job_title = form.data.get("job_title")
        address = form.data.get("address")
        organization = form.data.get("organization")

        # Validate first_name (allow only alphabets)
        if not re.match("^[A-Za-z]+$", first_name):
            form.add_error('first_name', "First name can only contain alphabets.")
            return render(request, "sales_tracker/agentcontact.html", {"form": form, "timer": formated_timer, "calling_agents": CallingAgent.objects.all()})

        # Validate last_name (allow only alphabets)
        if not re.match("^[A-Za-z]+$", last_name):
            form.add_error('last_name', "Last name can only contain alphabets.")
            return render(request, "sales_tracker/agentcontact.html", {"form": form, "timer": formated_timer, "calling_agents": CallingAgent.objects.all()})

        # Validate contact_number (must be exactly 10 digits)
        if not re.match(r"^\d{10}$", contact_number):
            form.add_error('contact_number', "Contact number must be exactly 10 digits.")
            return render(request, "sales_tracker/agentcontact.html", {"form": form, "timer": formated_timer, "calling_agents": CallingAgent.objects.all()})

        # Validate job_title (allow only alphabets and numbers)
        if not re.match("^[A-Za-z0-9 ]+$", job_title):
            form.add_error('job_title', "Job title can only contain alphabets and numbers.")
            return render(request, "sales_tracker/agentcontact.html", {"form": form, "timer": formated_timer, "calling_agents": CallingAgent.objects.all()})

        # If all validations pass, proceed to save the data
        try:
            ContactData.objects.get(email_id=email_id)
        except ContactData.DoesNotExist:
            # assigned_agent = assign_contact_to_agent()
            contact_details = ContactData(
                first_name=first_name,
                last_name=last_name,
                email_id=email_id,
                contact_number=contact_number,
                job_title=job_title,
                address=address,
                organization=MiningData.objects.get(organisation_name=organization),
                date=now_date,
                # assigned_to=assigned_agent.user,
                # calling_agent=CallingAgent.objects.get(calling_agent_id=claid),
            )
            contact_details.save()

            print("Contact successfully created.")
            return redirect("agentcontact")

        return render(request, "sales_tracker/agentcontact.html", {"form": form, "timer": formated_timer, "calling_agents": CallingAgent.objects.all()})

    else:
        form = ContactForm()

    return render(request, "sales_tracker/agentcontact.html", {"form": form, "timer": formated_timer, "calling_agents": CallingAgent.objects.all()})



import re
from django.shortcuts import render, redirect
from .forms import QuoteForm
from .models import QuotesData, OpportunityData
from django.contrib.auth import get_user_model
import datetime

def Agentquote(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs": int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"

    if request.method == "POST":
        form = QuoteForm(request.POST)

        title = form.data.get("title")
        lead_source = form.data.get("lead_source")
        account = form.data.get("account")
        contact = form.data.get("contact")
        total = form.data.get("total")
        sub_total = form.data.get("sub_total")
        grandtotal = form.data.get("grandtotal")
        discount = form.data.get("discount")
        shipping_tax = form.data.get("shipping_tax")
        tax = form.data.get("tax")

        # Validate title (allow only alphabets and numbers)
        if not re.match("^[A-Za-z ]+$", title):
           form.add_error('title', "Title can only contain alphabets.")
        
        # Validate lead_source (allow only alphabets and numbers)
        if not re.match("^[A-Za-z0-9 ]+$", lead_source):
            form.add_error('lead_source', "Lead source can only contain alphabets and numbers.")
        
        # Validate account (allow only alphabets and numbers)
        if not re.match("^[A-Za-z0-9 ]+$", account):
            form.add_error('account', "Account can only contain alphabets and numbers.")

        # Validate contact (must be exactly 10 digits)
        if not re.match(r"^\d{10}$", contact):
            form.add_error('contact', "Contact number must be exactly 10 digits.")
        
     # Validate total, sub_total, and grandtotal (allow only numbers or empty)
        if total and not re.match("^[0-9]+$", total):
            form.add_error('total', "Total can only contain numbers.")
        if sub_total and not re.match("^[0-9]+$", sub_total):
            form.add_error('sub_total', "Sub Total can only contain numbers.")
        if grandtotal and not re.match("^[0-9]+$", grandtotal):
            form.add_error('grandtotal', "Grand Total can only contain numbers.")

        
        # Validate discount, shipping_tax, and tax (allow numbers and special characters)
        if not re.match("^[\d\s.,-]+$", discount):
            form.add_error('discount', "Discount can only contain numbers and special characters.")
        if not re.match("^[\d\s.,-]+$", shipping_tax):
            form.add_error('shipping_tax', "Shipping Tax can only contain numbers and special characters.")
        if not re.match("^[\d\s.,-]+$", tax):
            form.add_error('tax', "Tax can only contain numbers and special characters.")

        # If there are validation errors, re-render the form with errors
        if form.errors:
            return render(request, "sales_tracker/agentquote.html", {"form": form, "timer": formated_timer})

        # If all validations pass, proceed to save the quote data
        quote_details = QuotesData(
            title=title,
            valid_until=form.data.get("valid_until"),
            approval_status=form.data.get("approval_status"),
            opportunity=OpportunityData.objects.get(pk=form.data.get("opportunity")),
            quote_stage=form.data.get("quote_stage"),
            invoice_status=form.data.get("invoice_status"),
            approval_issues_description=None if form.data.get("approval_issues_description") == "" else form.data.get("approval_issues_description"),
            lead_source=lead_source,
            account=account,
            contact=contact,
            billing_address=form.data.get("billing_address"),
            shipping_address=form.data.get("shipping_address"),
            total=total,
            discount=discount,
            sub_total=sub_total,
            shipping=form.data.get("shipping"),
            shipping_tax=shipping_tax,
            tax=tax,
            grandtotal=grandtotal,
            date=now_date,
            assigned_to=get_user_model().objects.get(username=request.user.username)
        )
        quote_details.save()

        return redirect("agentquote")

    else:
        form = QuoteForm()

    return render(request, "sales_tracker/agentquote.html", {"form": form, "timer": formated_timer})

import re
import datetime
from django.shortcuts import render, redirect
from .forms import OpportunityForm
from .models import OpportunityData, LeadsData
from django.contrib.auth import get_user_model

def Agentopportunity(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formatted_timer = {"hrs": int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"

    if request.method == "POST":
        form = OpportunityForm(request.POST)

        # Validate opportunity_name (allow only alphabets and numbers)
        opportunity_name = form.data.get("opportunity_name")
        if not re.match("^[A-Za-z0-9 ]+$", opportunity_name):
            form.add_error('opportunity_name', "Opportunity name can only contain alphabets and numbers.")

        # Validate amount (must be a positive number)
        amount = form.data.get("amount")
        if not re.match(r"^(0|[1-9]\d*)(\.\d+)?$", amount):  # Matches positive integers and decimals
            form.add_error('amount', "Amount must be a positive number.")

        # Validate probability (must be a positive number between 0 and 100)
        probability = form.data.get("probability")
        if not re.match(r"^(0|[1-9]\d?|100)(\.\d+)?$", probability):  # Matches numbers 0-100
            form.add_error('probability', "Probability must be a positive number between 0 and 100.")

        # Validate next_step (allow only alphabets and numbers)
        next_step = form.data.get("next_step")
        if not re.match("^[A-Za-z0-9 ]+$", next_step):
            form.add_error('next_step', "Next step can only contain alphabets and numbers.")

        # Validate lead_source (allow only alphabets and numbers)
        lead_source = form.data.get("lead_source")
        if not re.match("^[A-Za-z0-9 ]+$", lead_source):
            form.add_error('lead_source', "Lead source can only contain alphabets and numbers.")

        # Validate expected_close_date (must be a valid date)
        expected_close_date_str = form.data.get("expected_close_date")
        try:
            expected_close_date = datetime.datetime.strptime(expected_close_date_str, "%Y-%m-%d").date()
        except ValueError:
            form.add_error('expected_close_date', "Expected close date must be in YYYY-MM-DD format.")

        # If there are validation errors, re-render the form with errors
        if form.errors:
            return render(request, "sales_tracker/agentopportunity.html", {"form": form, "timer": formatted_timer})

        username = request.user.username
        contact_details = OpportunityData(
            opportunity_name=opportunity_name,
            amount=amount,
            sales_stage=form.data.get("sales_stage"),
            probability=probability,
            next_step=next_step,
            description=form.data.get("description"),
            expected_close_date=expected_close_date,  # Save the valid date
            lead_source=lead_source,
            lead=LeadsData.objects.get(pk=form.data.get("lead")),
            date=now_date,
            assigned_to=get_user_model().objects.get(username=username)
        )
        contact_details.save()

        return redirect("agentopportunity")

    else:
        form = OpportunityForm()

    return render(request, "sales_tracker/agentopportunity.html", {"form": form, "timer": formatted_timer})


import re
from django.shortcuts import render, redirect
from .forms import LeadForm
from .models import LeadsData, ContactData
import datetime

def Agentlead(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs": int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"

    if request.method == "POST":
        form = LeadForm(request.POST)
        
        lead_name = form.data.get("lead_name")
        first_name = form.data.get("first_name")
        last_name = form.data.get("last_name")
        email_id = form.data.get("email_id")
        contact_number = form.data.get("contact_number")
        job_title = form.data.get("job_title")
        address = form.data.get("address")
        contact_link = form.data.get("contact_link")
        nextdate = form.data.get("nextdate")
        remarks = form.data.get("remarks")

        # Validate first_name (allow only alphabets)
        if not re.match("^[A-Za-z]+$", first_name):
            form.add_error('first_name', "First name can only contain alphabets.")
            return render(request, "sales_tracker/agentlead.html", {"form": form, "timer": formated_timer})

        # Validate last_name (allow only alphabets)
        if not re.match("^[A-Za-z]+$", last_name):
            form.add_error('last_name', "Last name can only contain alphabets.")
            return render(request, "sales_tracker/agentlead.html", {"form": form, "timer": formated_timer})

        # Validate contact_number (must be exactly 10 digits)
        if not re.match(r"^\d{10}$", contact_number):
            form.add_error('contact_number', "Contact number must be exactly 10 digits.")
            return render(request, "sales_tracker/agentlead.html", {"form": form, "timer": formated_timer})

        # Validate job_title (allow only alphabets and numbers)
        if not re.match("^[A-Za-z0-9 ]+$", job_title):
            form.add_error('job_title', "Job title can only contain alphabets and numbers.")
            return render(request, "sales_tracker/agentlead.html", {"form": form, "timer": formated_timer})

        # If all validations pass, proceed to save the data
        try:
            LeadsData.objects.get(contact_link=ContactData.objects.get(pk=contact_link))
        except LeadsData.DoesNotExist:
            assign_lead = assign_leadCt()
            contact_details = LeadsData(
                lead_name=lead_name,
                first_name=first_name,
                last_name=last_name,
                email_id=email_id,
                contact_number=contact_number,
                job_title=job_title,
                address=address,
                contact_link=ContactData.objects.get(pk=contact_link),
                date=now_date,
                assigned_to=assign_lead,
                created_by=user,
                nextdate=nextdate,
                remarks=remarks
            )
            print("Lead successfully created.")
            contact_details.save()
            return redirect("agentlead")
        
        return render(request, "sales_tracker/agentlead.html", {"form": form, "timer": formated_timer})

    else:
        form = LeadForm()

    return render(request, "sales_tracker/agentlead.html", {"form": form, "timer": formated_timer})

def Agentmining(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    today_mining = MiningData.objects.filter(date = now_date)
    today_mining_count = today_mining.count()
    if request.method == "POST":
        form = MiningForm(request.POST)
        try:
            MiningData.objects.get(organisation_name = form.data.get("organisation_name"))
            print("hello world")
        except:
            assignTo = assign_miningCt()
            now_date_time = datetime.datetime.now()
            now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
            username = request.user.username
            mining_details = MiningData(
                organisation_name = form.data.get("organisation_name"),
                customer_first_name = form.data.get("customer_first_name"),
                customer_last_name = form.data.get("customer_last_name"),
                customer_address = form.data.get("customer_address"),
                customer_contact_number = form.data.get("customer_contact_number"),
                customer_mobile_number = form.data.get("customer_mobile_number"),
                customer_email = form.data.get("customer_email"),
                company_revenue = form.data.get("company_revenue"),
                company_emp_size = form.data.get("company_emp_size"),
                customer_offering = form.data.get("customer_offering"),
                competition_of_AT = form.data.get("competition_of_AT"),
                stock_market_registered = form.data.get("stock_market_registered"),
                influncer = form.data.get("influncer") == "on",
                desition_maker = form.data.get("desition_maker") == "on",
                IT_spending_budget = form.data.get("IT_spending_budget"),
                source_of_data_mining = form.data.get("source_of_data_mining"),
                date = now_date,
                assigned_to = assignTo,
                created_by = user,
            )
            mining_details.save()
            print("Hello world 4")
            return redirect("agentmining")    
        
        print("Hello world 2")
        return render(request, "sales_tracker/agentmining.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


    else:
        form = MiningForm()
    return render(request, "sales_tracker/agentmining.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


def Admindevice(request):
      return render(request, "sales_tracker/deviceAdmin.html")


import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DailySalesReportForm  # Make sure to create this form in forms.py
from .models import DailySalesReport  # Assuming you have a DailySalesReport model

def AgentDSR(request):


    if request.method == 'POST':
        form = DailySalesReportForm(request.POST)
        if form.is_valid():
            # Validate fields as per your requirements
            name = form.cleaned_data['name']
            if not re.match("^[A-Za-z ]+$", name):
                messages.error(request, "Name can only contain alphabets and spaces.")
                return render(request, 'sales_tracker/agent_report.html', {'form': form})

            customer_type = form.cleaned_data['customer_type']
            if not re.match("^[A-Za-z ]+$", customer_type):
                messages.error(request, "Customer Type can only contain alphabets and spaces.")
                return render(request, 'sales_tracker/agent_report.html', {'form': form})

            call_type = form.cleaned_data['call_type']
            if not re.match("^[A-Za-z ]+$", call_type):
                messages.error(request, "Call Type can only contain alphabets and spaces.")
                return render(request, 'sales_tracker/agent_report.html', {'form': form})

            # Ensure numeric fields are positive
            unit_cost = form.cleaned_data['unit_cost']
            quantity = form.cleaned_data['quantity']
            amount = form.cleaned_data['amount']
            tax_rate = form.cleaned_data['tax_rate']
            tax = form.cleaned_data['tax']
            total = form.cleaned_data['total']

            if unit_cost < 0 or quantity < 0 or amount < 0 or tax_rate < 0 or tax < 0 or total < 0:
                messages.error(request, "All numeric fields must be positive numbers.")
                return render(request, 'sales_tracker/agent_report.html', {'form': form})

            # Create and save the DailySalesReport instance
            report = DailySalesReport(
                name=name,
                customer_type=customer_type,
                call_type=call_type,
                date=form.cleaned_data['date'],
                time=form.cleaned_data['time'],
                item_number=form.cleaned_data['item_number'],
                item_name=form.cleaned_data['item_name'],
                item_description=form.cleaned_data['item_description'],
                unit_cost=unit_cost,
                quantity=quantity,
                amount=amount,
                tax_rate=tax_rate,
                tax=tax,
                total=total,
                notes=form.cleaned_data['notes'],
            )
            report.save()

            messages.success(request, "Daily Sales Report submitted successfully!")
            return redirect('some_view_name')  # Replace 'some_view_name' with the view you want to redirect to
        else:
            messages.error(request, "There was an error in your submission. Please check the form.")
    else:
        form = DailySalesReportForm()

    return render(request, "sales_tracker/agentDsr.html")



# def deviceAdmin(request):
    # context = {
    #     "id": "1",
    #     "uptime": "7:00:00",
    #     "downtime": "1:00:00",
    #     "ip": "192.168.123.1"
    # }
    # return render(request, 'sales_tracker/deviceAdmin.html', context)
  
def Admin_active(request):
    context = {
        "id": "1",
        "uptime": "7:00:00",
        "downtime": "1:00:00",
        "ip": "192.168.123.1",

        "id2": "2",
        "eid2": "02",
        "ename2": "rohit" ,
        "uptime2": "8:00:00",
        "downtime2": "1:00:00",
        "ip2": "192.168.123.1",

        "id3": "3",
        "eid3": "03",
        "ename3": "rohit" ,
        "uptime3": "9:00:00",
        "downtime3": "1:00:00",
        "ip3": "192.168.123.1"
    }
    return render(request, 'sales_tracker/adminActive.html', context)  

def Admin_passive(request):
    context = {
        "id": "1",
        "uptime": "7:00:00",
        "downtime": "1:00:00",
        "ip": "192.168.123.1",

        "id2": "2",
        "eid2": "02",
        "ename2": "rohit" ,
        "uptime2": "8:00:00",
        "downtime2": "1:00:00",
        "ip2": "192.168.123.1",

        "id3": "3",
        "eid3": "03",
        "ename3": "rohit" ,
        "uptime3": "9:00:00",
        "downtime3": "1:00:00",
        "ip3": "192.168.123.1"
     }
    return  render(request, 'sales_tracker/adminPassive.html', context)  


def Dsrview(request):

    return render(request, "sales_tracker/dsrview.html")


from django.shortcuts import render, redirect

def DSR(request):
    if request.method == 'POST':
        # Process form data here
        return redirect('your_view_name')  # Redirect to the same page
    return render(request, 'sales_tracker/dsr.html')




from django.shortcuts import render, redirect

from django.contrib import messages
from .forms import AccountForm
from .models import Account 

from .forms import PasswordForm
from .models import NewPasswords
from django.core.exceptions import ValidationError


def validate_password_view(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            # Get the entered password from the form
            entered_minor_password = form.cleaned_data['Minor_password']
            entered_sales_password = form.cleaned_data['Sales_password']
            entered_admin_password = form.cleaned_data['Admin_password']



            return redirect('createTask')  # 'createTask' should be the name of the URL pattern
    else:
        form = TaskForm()

    return render(request, 'sales_tracker/createTask.html', {'form': form})

def viewTask(request):
    return render(request, "sales_tracker/viewTask.html")

import re
from django.shortcuts import render, redirect
from .forms import AccountForm  # Assuming you have AccountForm in forms.py
from .models import Account  # Assuming you have Account model in models.py
from django.contrib import messages

def Agentaccount(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['Name']

            # Validate Name (allow only alphabets and spaces)
            if not re.match("^[A-Za-z ]+$", name):
                messages.error(request, "Name can only contain alphabets and spaces.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Validate Billing fields (allow only alphabets, numbers, and special characters like , and .)
            billing_street = form.cleaned_data['Billing_Street']
            if not re.match("^[A-Za-z0-9 ,\.]+$", billing_street):
                messages.error(request, "Billing Street can only contain alphabets, numbers, commas, and periods.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            billing_city = form.cleaned_data['Billing_City']
            if not re.match("^[A-Za-z0-9 ,\.]+$", billing_city):
                messages.error(request, "Billing City can only contain alphabets, numbers, commas, and periods.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            billing_state = form.cleaned_data['Billing_State']
            if not re.match("^[A-Za-z0-9 ,\.]+$", billing_state):
                messages.error(request, "Billing State can only contain alphabets, numbers, commas, and periods.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            billing_country = form.cleaned_data['Billing_Country']
            if not re.match("^[A-Za-z0-9 ,\.]+$", billing_country):
                messages.error(request, "Billing Country can only contain alphabets, numbers, commas, and periods.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Validate Billing Postal Code (allow only numbers)
            billing_postal_code = form.cleaned_data['Billing_Postal_Code']
            if not re.match("^\d+$", billing_postal_code):
                messages.error(request, "Billing Postal Code can only contain numbers.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Validate Shipping fields (allow only alphabets, numbers, and special characters like , and .)
            shipping_street = form.cleaned_data['Shipping_Street']
            if not re.match("^[A-Za-z0-9 ,\.]+$", shipping_street):
                messages.error(request, "Shipping Street can only contain alphabets, numbers, commas, and periods.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            shipping_city = form.cleaned_data['Shipping_City']
            if not re.match("^[A-Za-z0-9 ,\.]+$", shipping_city):
                messages.error(request, "Shipping City can only contain alphabets, numbers, commas, and periods.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            shipping_state = form.cleaned_data['Shipping_State']
            if not re.match("^[A-Za-z0-9 ,\.]+$", shipping_state):
                messages.error(request, "Shipping State can only contain alphabets, numbers, commas, and periods.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            shipping_country = form.cleaned_data['Shipping_Country']
            if not re.match("^[A-Za-z0-9 ,\.]+$", shipping_country):
                messages.error(request, "Shipping Country can only contain alphabets, numbers, commas, and periods.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Validate Shipping Postal Code (allow only numbers)
            shipping_postal_code = form.cleaned_data['Shipping_Postal_Code']
            if not re.match("^\d+$", shipping_postal_code):
                messages.error(request, "Shipping Postal Code can only contain numbers.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Validate Description (allow only alphabets and numbers)
            description = form.cleaned_data['Description']
            if not re.match("^[A-Za-z0-9 ]+$", description):
                messages.error(request, "Description can only contain alphabets and numbers.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Validate Assigned To (allow only alphabets and numbers)
            assigned_to = form.cleaned_data['Assigned_To']
            if not re.match("^[A-Za-z0-9 ]+$", assigned_to):
                messages.error(request, "Assigned To can only contain alphabets and numbers.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Validate Type (allow only alphabets and numbers)
            account_type = form.cleaned_data['Type']
            if not re.match("^[A-Za-z0-9 ]+$", account_type):
                messages.error(request, "Type can only contain alphabets and numbers.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Validate Member Of (allow only alphabets and numbers)
            member_of = form.cleaned_data['Member_Of']
            if not re.match("^[A-Za-z0-9 ]+$", member_of):
                messages.error(request, "Member Of can only contain alphabets and numbers.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Validate Campaign (allow only alphabets and numbers)
            campaign = form.cleaned_data['Campaign']
            if not re.match("^[A-Za-z0-9 ]+$", campaign):
                messages.error(request, "Campaign can only contain alphabets and numbers.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Validate Industry (allow only alphabets and numbers)
            industry = form.cleaned_data['Industry']
            if not re.match("^[A-Za-z0-9 ]+$", industry):
                messages.error(request, "Industry can only contain alphabets and numbers.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Validate Employees (must be a non-negative integer)
            employees = form.cleaned_data['Employees']
            if not isinstance(employees, int) or employees < 0:  
                messages.error(request, "Employees must be a non-negative integer.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Validate Annual Revenue (must be a positive number)
            annual_revenue = form.cleaned_data['Annual_Revenue']
            if annual_revenue is None or annual_revenue <= 0:
                messages.error(request, "Annual Revenue must be a positive number.")
                return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # Create the Account object and save it to the database
            account = Account(
                Name=name,
                Website=form.cleaned_data['Website'],
                Email_Address=form.cleaned_data['Email_Address'],
                Billing_Street=billing_street,
                Billing_Postal_Code=billing_postal_code,
                Billing_City=billing_city,
                Billing_State=billing_state,
                Billing_Country=billing_country,
                Description=description,
                Assigned_To=assigned_to,
                Shipping_Street=shipping_street,
                Shipping_Postal_Code=shipping_postal_code,
                Shipping_City=shipping_city,
                Shipping_State=shipping_state,
                Shipping_Country=shipping_country,
                Type=account_type,
                Annual_Revenue=annual_revenue,
                Member_Of=member_of,
                Campaign=campaign,
                Industry=industry,
                Employees=employees,
            )
            account.save()  # Save the account instance

            messages.success(request, "Account created successfully!")
            return redirect('agentaccount')  # Redirect to the account list page after successful submission
        else:
            messages.error(request, "There was an error creating the account. Please check the form.")
    else:
        form = AccountForm()

    return render(request, 'sales_tracker/agentaccount.html', {'form': form})

            # account.save() 
def viewAccount(request):
    return render(request, "sales_tracker/viewaccount.html")


class AgentMeeting(View):
    def get(self, request):
        form = agentmeeting()
        return render(request, 'sales_tracker/agentmeeting.html', {'form': form})

    def post(self, request):
        form = agentmeeting(request.POST)
        if form.is_valid():
            # Save the form data to the database
            print("FOrm is valid")
            form.save()

        return render(request, 'sales_tracker/agentmeeting.html', {'form': form})
    



def createDocument(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')
    else:
        form = DocumentForm()
    
    return render(request, 'sales_tracker/createDocument.html', {'form': form})

def viewDocument(request):

    return render(request, "sales_tracker/viewDocument.html")



#     def post(self, request):
#         form = agentcalling(request.POST)
#         if form.is_valid():
#             # Save the form data to the database
#             form.save()
#             print("Form is valid")
#         else:
#             print("Form errors: ", form.errors)

#         return render(request, 'sales_tracker/agentcalling.html', {'form': form})


class ViewScheduledCalls(View):
    def get(self, request):
        scheduled_calls = Schedule_Calling.objects.all()
        return render(request, 'sales_tracker/view_calling.html', {'scheduled_calls': scheduled_calls})


def schedule_calling_create(request):
    if request.method == 'POST':
        form = Schedule_Calling(request.POST)
        if form.is_valid():
            print("this is valid form")
            form.save()
    else:
        form = Schedule_Calling()
    return render(request, 'sales_tracker/agentcalling.html', {'form': form})

class AgentCalling(View):
    def get(self, request):
        form = agentcalling()
        return render(request, 'sales_tracker/agentcalling.html', {'form': form})

    def post(self, request):
        form = agentcalling(request.POST)
        if form.is_valid():
            # Save the form data to the database
            print("FOrm is valid")
            form.save()

        return render(request, 'sales_tracker/agentcalling.html', {'form': form})


 
def ViewScheduledMeeting(request):
    scheduled_meetings = Schedule_Meeting.objects.all()
    return render(request, 'sales_tracker/view_meeting.html', {'scheduled_meetings': scheduled_meetings})



from django.shortcuts import render, redirect
from .forms import TaskForm

def createNotes(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('note_list')  # Replace 'note_list' with your desired redirect URL
    else:
        form = NoteForm()
    
    return render(request, 'sales_tracker/createNotes.html', {'form': form})

def liveStreaming(request):
    return render(request, "sales_tracker/liveStreaming.html")

def viewcontact(request):
    return render(request, "sales_tracker/viewcontact.html")

def leadImport(request):
    return render(request, "sales_tracker/leadImport.html")

def contactImport(request):
    return render(request, "sales_tracker/contactImport.html")

def quotesImport(request):
    return render(request, "sales_tracker/quoteimport.html")

def opportunityimport(request):
    return render(request, "sales_tracker/opportunityimport.html")

def accountimport(request):
    return render(request, "sales_tracker/accountimport.html")

def DSRimport(request):
    return render(request, "sales_tracker/DSRimport.html")


from django.shortcuts import render, redirect
from .forms import TaskForm

from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm  # Import TaskForm if defined in forms.py

def createTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            # Redirect to the same page or a success page
            return redirect('create_task')  # Use the appropriate URL name
    else:
        form = TaskForm()

    return render(request, "sales_tracker/createTask.html"
                  , {'form': form})





def temp(request):
    return render(request, 'sales_tracker/temp.html')

def send_meeting_email(request, meeting_id):
    meeting = get_object_or_404(Schedule_Meeting, id=meeting_id)
    subject = "Meeting Reminder"
    message = f"Dear {meeting.assigned_to},\n\nThis is a reminder for your meeting.\n\nDetails:\nSubject: {meeting.subject}\nStart Date: {meeting.start_date}\nEnd Date: {meeting.end_date}\nStart Time: {meeting.start_time}\nEnd Time: {meeting.end_time}\n\nBest regards,\nAapai Technology."
    recipient_list = [meeting.contact]

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        return HttpResponse("Email sent successfully!")
    except Exception as e:
        return HttpResponse(f"Failed to send email: {e}")


def miningimport(request):
    return render(request, "sales_tracker/miningimport.html")



def viewNotes(request):
      return render(request, "sales_tracker/viewNotes.html")

from django.shortcuts import render, redirect
from django.views.generic import CreateView
# from .models import Opportunity
from .forms import OpportunityForm

from django.shortcuts import render, redirect
from .forms import InvoiceForm

def createInvoices(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            # Here you could handle the form data manually if needed
            # For now, we'll just redirect as if it was saved
            return redirect('invoice_list')  # Adjust redirect target as needed
    else:
        form = InvoiceForm()
    return render(request, 'sales_tracker/createInvoices.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ComposeEmailForm  # Import your ComposeEmailForm class
import datetime

def compose_email(request):
    """
    This view handles the email composition form.
    If the request is POST, it validates and processes the form data.
    On GET requests, it displays the empty form for the user to fill out.
    """
    if request.method == 'POST':
        form = ComposeEmailForm(request.POST)
        if form.is_valid():
            # Process the form data (e.g., save to the database or send an email)
            # Placeholder for processing logic, e.g., saving or sending the email
            email_template = form.cleaned_data.get('template')
            related_to = form.cleaned_data.get('related_to')
            from_address = form.cleaned_data.get('from')
            to_address = form.cleaned_data.get('to')
            cc_address = form.cleaned_data.get('cc')
            bcc_address = form.cleaned_data.get('bcc')
            subject = form.cleaned_data.get('subject')
            body = form.cleaned_data.get('body')
            send_plain_text = form.cleaned_data.get('send_plain_text')

            # Here you could save the email details to a model or send it directly

            messages.success(request, 'Email composed successfully!')
            return redirect('agentemail')  # Redirect to the same page or another view
        else:
            messages.error(request, 'There was an error composing the email. Please check your input.')
    else:
        form = ComposeEmailForm()  # Initialize an empty form for a GET request

    return render(request, 'sales_tracker/agentemail.html', {'form': form})



def viewEmail(request):
    return render(request, "sales_tracker/viewemail.html")


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def Agenttarget(request):
    """
    This view handles the contact form submission.
    If the request is POST, it validates and processes the form data.
    On GET requests, it displays the empty form for the user to fill out.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data, e.g., save to the database or send notification
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            job_title = form.cleaned_data.get('job_title')
            office_phone = form.cleaned_data.get('office_phone')
            department = form.cleaned_data.get('department')
            mobile = form.cleaned_data.get('mobile')
            account_name = form.cleaned_data.get('account_name')
            fax = form.cleaned_data.get('fax')
            primary_address_street = form.cleaned_data.get('primary_address_street')
            primary_address_postal_code = form.cleaned_data.get('primary_address_postal_code')
            primary_address_city = form.cleaned_data.get('primary_address_city')
            primary_address_state = form.cleaned_data.get('primary_address_state')
            primary_address_country = form.cleaned_data.get('primary_address_country')
            other_address_street = form.cleaned_data.get('other_address_street')
            other_address_postal_code = form.cleaned_data.get('other_address_postal_code')
            other_address_city = form.cleaned_data.get('other_address_city')
            other_address_state = form.cleaned_data.get('other_address_state')
            other_address_country = form.cleaned_data.get('other_address_country')
            email_address = form.cleaned_data.get('email_address')
            description = form.cleaned_data.get('description')
            assigned_to = form.cleaned_data.get('assigned_to')

            # Save or process form data here

            messages.success(request, 'Contact information submitted successfully!')
            return redirect('agenttarget')  # Redirect to the same page or another view
        else:
            messages.error(request, 'There was an error submitting the contact information. Please check your input.')
    else:
        form = ContactForm()  # Initialize an empty form for a GET request

    return render(request, 'sales_tracker/agenttarget.html', {'form': form})

def viewInvoices(request):
    return render(request, 'sales_tracker/viewInvoices.html')

