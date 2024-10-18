# from typing import Any
# from django.db.models.query import QuerySet
import json
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
from .models import MiningData, ContactData, LeadsData, OpportunityData, QuotesData , CallingAgent,Schedule_Meeting
from .forms import MiningForm, ContactForm, LeadForm, OpportunityForm, QuoteForm, agentmeeting, ScheduleCallingForm

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
# from .forms import agentcalling
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


# Create your views here.
# class IndexView(TemplateView):
#     template_name = "sales_tracker/index.html"
#     def dispatch(self, request, *args, **kwargs):
#         if self.request.user.profile.branch != 'miner': 
#             return HttpResponseForbidden("You do not have access to this page.")
#         return super().dispatch(request, *args, **kwargs)
#     # def dispatch(self, request, *args, **kwargs):
#     #     print("Thisis ")
#     #     if self.request.user.profile.branch == 'agent': 
#     #         self.template_name = "sales_tracker/agent.html"
#     #     return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context =  super().get_context_data(**kwargs)
#         request = self.request
#         user = request.user
#         context["user"] = user.username
#         utc_login_time = user.last_login
#         elapsed_time = timer(utc_login_time)
#         context["timer"] = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
#         now_date_time = datetime.datetime.now()
#         now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
#         today_mining = MiningData.objects.filter(date = now_date)
#         today_mining_count = today_mining.count()
#         context["mining_count"] = today_mining_count
#         today_lead = LeadsData.objects.filter(date = now_date)
#         today_lead_count = today_lead.count()
#         context["lead_count"] = today_lead_count
#         today_contact = ContactData.objects.filter(date = now_date)
#         today_contact_count = today_contact.count()
#         context["contact_count"] = today_contact_count
#         today_Opportunity = OpportunityData.objects.filter(date = now_date)
#         today_Opportunity_count = today_Opportunity.count()
#         context["Opportunity_count"] = today_Opportunity_count
#         return context



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



# @admin_required
# class Admin(TemplateView):
#     template_name = "sales_tracker/admin.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         attendances = AttendanceRecord.objects.all()
#         att = Att_perct()
#         late = Late_perct()
#         context['admin_message'] = "Welcome to the Admin Page"
#         context['attendances'] = attendances
#         context['att'] = att
#         context['late'] = Late_perct 
#         return context
    

# class Agent(TemplateView):
#     template_name = "sales_tracker/agent.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         request = self.request
#         users = request.user
#         u = RegisterUser.objects.get(email=users)
#         u = u.id
#         ToCall = MiningData.objects.filter(assigned_to=u)
#         context["user"] = u
#         context["Tocall"] = ToCall
#         return context


# class MiningView(CreateView):
#     model = MiningData
#     form_class = MiningForm
#     template_name = "sales_tracker/mining.html"
#     success_url = "mining"
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
    


# def assign_miningCt():
#     # user = request.user
#     least_occurring_assigned_to_id = (
#     MiningData.objects
#     .filter(assigned_to__profile__branch='agent')
#     .values('assigned_to')
#     .annotate(count=Count('assigned_to'))
#     .order_by('count')
#     .first()
# )
#     # return least_occurring_assigned_to_id
#     assigned_to_id = least_occurring_assigned_to_id['assigned_to']
#     return RegisterUser.objects.get(id=assigned_to_id)




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






# def assign_miningCt():
#     # Get IDs of profiles with branch='agent'
#     agent_profile_ids = Profile.objects.filter(branch='agent').values_list('user_id', flat=True)
    
#     # Subquery to get the least occurring assigned_to ID
#     least_occurring_subquery = MiningData.objects.filter(
#         assigned_to__in=agent_profile_ids
#     ).values('assigned_to').annotate(count=Count('assigned_to')).order_by('count').values('assigned_to')[:1]

#     # Use the subquery to get the least occurring assigned_to
#     least_occurring_assigned_to_id = Subquery(least_occurring_subquery)

#     # Get the corresponding RegisterUser
#     assigned_to_user = RegisterUser.objects.filter(
#         user_id=least_occurring_assigned_to_id
#     ).first()

#     return assigned_to_user


# ---------------------------------------------------------------------
# def assign_miningCt():
#     # Raw SQL query to find the least occurring `assigned_to` ID
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT M.assigned_to_id
#             FROM sales_tracker_miningdata as M
#             LEFT JOIN users_profile as P
#             ON M.assigned_to_id = P.user_id
#             WHERE P.branch = 'agent'
#             GROUP BY P.user_id
#             LIMIT 1;
#         """)
        
#         # Fetch the result
#         result = cursor.fetchone()
    
#     if result:
#         assigned_to_id = result[0]
#         # Fetch and return the RegisterUser object
#         return RegisterUser.objects.get(id=assigned_to_id)
#     else:
#         print("None is returned")
#         return None




# def assign_miningCt():
#     # Raw SQL query to find the least occurring `assigned_to` ID
#     with connection.cursor() as cursor:
#         cursor.execute("""
#             SELECT assigned_to_id
#             FROM sales_tracker_miningdata
#             JOIN users_registeruser ON sales_tracker_miningdata.assigned_to_id = users_registeruser.id
#             JOIN users_profile ON users_registeruser.id = users_profile.user_id
#             WHERE users_profile.branch = %s
#             GROUP BY assigned_to_id
#             ORDER BY COUNT(*) ASC
#             LIMIT 1
#         """, ['agent'])
        
#         # Fetch the result
#         result = cursor.fetchone()
#         if result:
#             assigned_to_id = result[0]
#             # Debugging: Print the fetched ID
#             print(f"Fetched assigned_to_id: {assigned_to_id}")
#             try:
#                 # Fetch and return the RegisterUser object
#                 return RegisterUser.objects.get(id=assigned_to_id)
#             except RegisterUser.DoesNotExist:
#                 # Handle case where the RegisterUser object is not found
#                 print(f"RegisterUser with id {assigned_to_id} does not exist.")
#                 return None
#         else:
#             print("No result returned from the query.")
#             return None



def mining_view(request):
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
        state = request.POST.get("state")
        city = request.POST.get("city")
        zone = request.POST.get("zone")

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
                state = state,
                city = city,
                region = zone,
            )
            mining_details.save()
            print("Hello world 4")
            return redirect("mining")    
        
        print("Hello world 2")
        return render(request, "sales_tracker/mining.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


    else:
        form = MiningForm()
    return render(request, "sales_tracker/mining.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})

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







# def get_call_center_data():
#     # Connect to the external MySQL database
#     connection = pymysql.connect(
#         host='localhost',        # Replace with your database host
#         user='root',    # Replace with your database username
#         password='Pj@123456',# Replace with your database password
#         database='CallCenter',           # Replace with your database name
#         port=3306                # Replace with your database port if different
#     )

#     try:
#         with connection.cursor(pymysql.cursors.DictCursor) as cursor:
#             # Execute an SQL query
#             sql = "SELECT * FROM CallingAgent"  # Replace with your SQL query
#             cursor.execute(sql)

#             # Fetch all the rows from the result
#             result = cursor.fetchall()
#             return result
#     finally:
#         connection.close()

# def call_center_view(request):
#     context = {}
#     data = get_call_center_data()
#     context['data'] = data
#     return render(request, "sales_tracker/call_center.html",context)
#     # return JsonResponse({'data': data})



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



# class Admin(TemplateView):
#     template_name = "sales_tracker/admin.html"
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         attendances = AttendanceRecord.objects.all()
#         att = Att_perct()
#         late = Late_perct()
#         context['admin_message'] = "Welcome to the Admin Page"
#         context['attendances'] = attendances
#         context['att'] = att
#         context['late'] = Late_perct 
#         return context


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

# class DailyAttendence(TemplateView):
#     DailyAttendance()
#     template_name = "sales_tracker/DailyAttendence.html"
    


# class maps(View):
#     template_name = "sales_tracker/maps.html"
#     def get(self,request):
#         context = {}
#         latitude = request.session.get('latitude')
#         longitude = request.session.get('longitude')
#         context['lat'] = latitude
#         context['long'] = longitude
#         return render(request, self.template_name, context)
    
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
# def get_salesperson_locations(request):
#     locations = Location.objects.all().values('salesperson__name', 'latitude', 'longitude', 'timestamp')
#     location_list = list(locations)
#     return JsonResponse(location_list, safe=False)

# >>>>>>> 16756faba89c5c4438801884b3e586a32b127c3e

#         # Save latitude and longitude to session
#         request.session['latitude'] = latitude
#         request.session['longitude'] = longitude

#         # Save to the database
#         profile = Profile.objects.get(user=request.user)
#         Location.objects.create(profile=profile, latitude=latitude, longitude=longitude)

#         return JsonResponse({'status': 'success'})

def ViewQuote(request):
    pass



def Agentcontact(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
  
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

            return redirect("agentcontact")
        
        return render(request, "sales_tracker/agentcontact.html", {"form":form, "timer": formated_timer, "calling_agents": CallingAgent.objects.all()})


    else:
        form = ContactForm()
    return render(request, "sales_tracker/agentcontact.html", {"form":form, "timer": formated_timer, "calling_agents": CallingAgent.objects.all()})



def Agentquote(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
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

        return redirect("agentquote")
    # return redirect("message")
        
        # return render(request, "sales_tracker/create_lead.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


    else:
        form = QuoteForm()
    return render(request, "sales_tracker/agentquote.html", {"form":form, "timer": formated_timer})



def Agentopportunity(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    # today_mining = MiningData.objects.filter(date = now_date)
    # today_mining_count = today_mining.count()
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

        return redirect("agentopportunity")
    #  return redirect("message")
        
        # return render(request, "sales_tracker/create_lead.html", {"form":form, "timer": formated_timer, "mining_count": today_mining_count})


    else:
        form = OpportunityForm()
    return render(request, "sales_tracker/agentopportunity.html", {"form":form, "timer": formated_timer})



def Agentlead(request):
    user = request.user
    utc_login_time = user.last_login
    elapsed_time = timer(utc_login_time)
    formated_timer = {"hrs":int(elapsed_time[0]), "min": int(elapsed_time[1]), "sec": int(elapsed_time[2])}
    now_date_time = datetime.datetime.now()
    now_date = f"{now_date_time.strftime('%Y')}-{now_date_time.strftime('%m')}-{now_date_time.strftime('%d')}"
    # today_mining = MiningData.objects.filter(date = now_date)
    # today_mining_count = today_mining.count()
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

            return redirect("agentlead")
        
        return render(request, "sales_tracker/agentlead.html", {"form":form, "timer": formated_timer})


    else:
        form = LeadForm()
    return render(request, "sales_tracker/agentlead.html", {"form":form, "timer": formated_timer})

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

def AdminDSR(request):

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


def DSR(request):

    return render(request, "sales_tracker/dsr.html")



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


            # Here you would typically save the task to the database
            # You could create a model instance for Task and save it
            # Example (assuming you have a Task model):
            # Task.objects.create(
            #     subject=subject,
            #     start_date=start_date,
            #     due_date=due_date,
            #     priority=priority,
            #     description=description,
            #     status=status,
            #     related_to=related_to,
            #     contacts=contacts
            # )

            # After saving or processing, redirect to another page (e.g., task list)
            return redirect('createTask')  # 'createTask' should be the name of the URL pattern
    else:
        form = TaskForm()

    return render(request, 'sales_tracker/createTask.html', {'form': form})

def viewTask(request):
    return render(request, "sales_tracker/viewTask.html")




def Agentaccount(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['Name']
            website = form.cleaned_data['Website']
            email_address = form.cleaned_data['Email_Address']
            billing_address = form.cleaned_data['Billing_Address']
            billing_street = form.cleaned_data['Billing_Street']
            billing_postal_code = form.cleaned_data['Billing_Postal_Code']
            billing_city = form.cleaned_data['Billing_City']
            billing_state = form.cleaned_data['Billing_State']
            billing_country = form.cleaned_data['Billing_Country']
            description = form.cleaned_data['Description']
            assigned_to = form.cleaned_data['Assigned_To']
            shipping_address = form.cleaned_data['Shipping_Address']
            shipping_street = form.cleaned_data['Shipping_Street']
            shipping_postal_code = form.cleaned_data['Shipping_Postal_Code']
            shipping_city = form.cleaned_data['Shipping_City']
            shipping_state = form.cleaned_data['Shipping_State']
            shipping_country = form.cleaned_data['Shipping_Country']
            account_type = form.cleaned_data['Type']
            annual_revenue = form.cleaned_data['Annual_Revenue']
            member_of = form.cleaned_data['Member_Of']
            campaign = form.cleaned_data['Campaign']
            industry = form.cleaned_data['Industry']
            employees = form.cleaned_data['Employees']

            account = Account(
                name=name,
                website=website,
                email_address=email_address,
                billing_address=billing_address,
                billing_street=billing_street,
                billing_postal_code=billing_postal_code,
                billing_city=billing_city,
                billing_state=billing_state,
                billing_country=billing_country,
                description=description,
                assigned_to=assigned_to,
                shipping_address=shipping_address,
                shipping_street=shipping_street,
                shipping_postal_code=shipping_postal_code,
                shipping_city=shipping_city,
                shipping_state=shipping_state,
                shipping_country=shipping_country,
                account_type=account_type,
                annual_revenue=annual_revenue,
                member_of=member_of,
                campaign=campaign,
                industry=industry,
                employees=employees,
            )
            # account.save() 

            # Retrieve the stored passwords from the database
            try:
                stored_passwords = NewPasswords.objects.first()  # Assuming you have only one instance of Passwords
                if not stored_passwords:
                    raise ValidationError("No passwords found in the database.")
                
                # Compare entered passwords with the ones in the database
                if (entered_minor_password == stored_passwords.Minor_password and
                    entered_sales_password == stored_passwords.Sales_password and
                    entered_admin_password == stored_passwords.Admin_password):
                    # If passwords match, you can proceed
                    return redirect('success_url')
                else:
                    # If passwords don't match, raise an error
                    form.add_error(None, 'Passwords do not match the stored passwords.')

            
            except NewPasswords.DoesNotExist:
                form.add_error(None, 'Stored passwords not found in the database.')
        
        # If form is invalid, re-render the form with errors
        return render(request, 'validate_password.html', {'form': form})

    else:
        form = PasswordForm()
    return render(request, 'validate_password.html', {'form': form})



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


# class ViewScheduledCalls(View):
#     def get(self, request):
#         scheduled_calls = Schedule_Calling.objects.all()
#         return render(request, 'sales_tracker/view_calling.html', {'scheduled_calls': scheduled_calls})


def schedule_calling_create(request):
    if request.method == 'POST':
        form = ScheduleCallingForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('schedule_calling_list')
    else:
        form = ScheduleCallingForm()
    return render(request, 'sales_tracker/agentcontact.html', {'form': form})
def ViewScheduledMeeting(request):
    scheduled_meetings = Schedule_Meeting.objects.all()
    return render(request, 'sales_tracker/view_meeting.html', {'scheduled_meetings': scheduled_meetings})
