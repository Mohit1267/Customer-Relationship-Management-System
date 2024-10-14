from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import get_salesperson_locations


urlpatterns = [
    path("", login_required(views.Dashboards), name="Dashboards"),
    # path("adminn", login_required(views.Admin.as_view()), name="adminn"),
    path('attendance/', (views.Attendence), name='attendance'),
    #path('maps',(views.maps.as_view()),name = 'maps'),
    # path("agent/", login_required(views.Agent.as_view()), name="agent"),
    path("agent/<pk>", login_required(views.DetailCalling), name="detail_agent"),
    path("sales/<pk>", login_required(views.DetailSales), name="detail_sales"),
    path("Attendence/", login_required(views.Attendence), name="attendance"),
    path("reports/", login_required(views.Admin_reports.as_view()), name="reports"),
    path("reports/MinerActivity/", login_required(views.MinerActivity.as_view()), name="MinerActivity"),
    # path("reports/DailyAttendence/", login_required(views.DailyAttendence.as_view()), name="DailyAttendence"),
    path("reports/MinerActivity/<pk>", login_required(views.EmployeeDetail.as_view()), name="EmployeeDetail"),
    path("reports/LeadsActivity/", login_required(views.LeadsActivity.as_view()), name="LeadsActivity"),
    path("reports/Analysis/", login_required(views.AdminAnalysis.as_view()), name="AdminAnalysis"),
    # path("view_quote")

    path("mining", login_required(views.mining_view), name = "mining"),
    path("data", login_required(views.DataView.as_view()), name = "data"),
    path("detail/<pk>", views.DetailDataView.as_view(), name = "detaildata"),
    path("call", views.CallView.as_view(), name = "call"),
    path("videocall", views.VideoCallView.as_view(), name = "videocall"),
    path("joinmeet", views.join_meet, name = "joinmeet"),
    path("createcontact", views.Create_contact_view, name = "create_contact"), 
    path("message", views.Message.as_view(), name = "message"), 
    path("createlead", views.Create_lead_view, name = "create_lead"), 
    path("lead_data", login_required(views.LeadView.as_view()), name = "lead_data"), 
    path("quotes_data", login_required(views.QuotesView.as_view()), name = "quotes_data"), 
    # path("quotes_data", login_required(views.QuotesView.as_view()), name = "view_quote"), 
    path("opp_data", login_required(views.OpportunityView.as_view()), name = "opp_data"), 
    path("opportunity_data", login_required(views.OpportunityView.as_view()), name = "opportunity_data"), 
    path("createopportunity", views.Create_opportunity_view, name = "create_opportunity"), 
    path("createquote", views.Create_quote_view, name = "create_quote"), 
    path("rev", views.MiningsView.as_view(), name = "view"), 
    path("tocall", views.Tocall.as_view(), name = "tocall"), 
    path("tocall/<pk>", views.Tocall_detail, name = "tocalldata"),
    path("cc", views.get_calling_agents, name ="cc"),
    path('get_timer/', login_required(views.get_timer_value), name='get_timer'),

    path("agentcontact", login_required(views.Agentcontact), name="agentcontact"),
    path("agentlead", login_required(views.Agentlead), name="agentlead"),
    path("agentquote", login_required(views.Agentquote), name="agentquote"),
    path("agentopportunity", login_required(views.Agentopportunity), name="agentopportunity"),
    path("agentmining", login_required(views.Agentmining), name="agentmining"),

    # path("agentmessage", views.Agentmessage.as_view(), name = "agentmessage"), 
    path("adminActive", login_required(views.Admin_active), name="adminActive"),
    path("adminPassive", login_required(views.Admin_passive), name="adminPassive"),
    # path("deviceAdmin", login_required(views.deviceAdmin), name="deviceAdmin"),
    path("adminActive", login_required(views.Admin_active), name="adminActive"),
    path("adminPassive", login_required(views.Admin_passive), name="adminPassive"),
    path("agentDsr", login_required(views.AdminDSR), name="agentDsr"),
    path("dsrview", login_required(views.Dsrview), name="dsrview"),
    path("DSR", login_required(views.DSR), name="DSR"),
    path("liveStreaming", login_required(views.liveStreaming), name="liveStreaming"),
    path("maps", login_required(views.maps), name="maps"),


    path('get-locations/', get_salesperson_locations, name='get_locations'),

]


'''urlpatterns = [
    path('get-locations/', get_salesperson_locations, name='get_locations'),
]
'''




