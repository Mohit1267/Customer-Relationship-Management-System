from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [

    path("", login_required(views.Dashboards), name="Dashboards"),
    path('attendance/', (views.Attendence), name='attendance'),
    path('maps',(views.maps.as_view()),name = 'maps'),
    path("agent/<pk>", login_required(views.DetailCalling), name="detail_agent"),
    path("sales/<pk>", login_required(views.DetailSales), name="detail_sales"),
    path("reports/", login_required(views.Admin_reports.as_view()), name="reports"),
    path("reports/MinerActivity/", login_required(views.MinerActivity.as_view()), name="MinerActivity"),
    path("reports/MinerActivity/<pk>", login_required(views.EmployeeDetail.as_view()), name="EmployeeDetail"),
    path("reports/LeadsActivity/", login_required(views.LeadsActivity.as_view()), name="LeadsActivity"),
    path("reports/Analysis/", login_required(views.AdminAnalysis.as_view()), name="AdminAnalysis"),
    path("mining", login_required(views.mining_view), name="mining"),
    path("data", login_required(views.DataView.as_view()), name="data"),
    path("detail/<pk>", login_required(views.DetailDataView.as_view()), name="detaildata"),
    path("call", login_required(views.CallView.as_view()), name="call"),
    path("videocall", login_required(views.VideoCallView.as_view()), name="videocall"),
    path("joinmeet", login_required(views.join_meet), name="joinmeet"),
    path("createcontact", login_required(views.Create_contact_view), name="create_contact"),
    path("message", login_required(views.Message.as_view()), name="message"),
    path("createlead", login_required(views.Create_lead_view), name="create_lead"),
    path("lead_data", login_required(views.LeadView.as_view()), name="lead_data"),
    path("quotes_data", login_required(views.QuotesView.as_view()), name="quotes_data"),
    path("opp_data", login_required(views.Create_opportunity_view), name="opp_data"),
    path("createopportunity", login_required(views.Create_opportunity_view), name="create_opportunity"),
    path("createquote", login_required(views.Create_quote_view), name="create_quote"),
    path("rev", login_required(views.MiningsView.as_view()), name="view"),
    path("tocall", login_required(views.Tocall.as_view()), name="tocall"),
    path("tocall/<pk>", login_required(views.Tocall_detail), name="tocalldata"),
    path("cc", login_required(views.get_calling_agents), name="cc"),
    path("get_timer/", login_required(views.get_timer_value), name="get_timer"),
    path("agentcontact", login_required(views.Agentcontact), name="agentcontact"),
    path("agentlead", login_required(views.Agentlead), name="agentlead"),
    path("agentquote", login_required(views.Agentquote), name="agentquote"),
    path("agentopportunity", login_required(views.Agentopportunity), name="agentopportunity"),
    path("agentmining", login_required(views.Agentmining), name="agentmining"),
    path("adminActive", login_required(views.Admin_active), name="adminActive"),
    path("adminPassive", login_required(views.Admin_passive), name="adminPassive"),
    path("agentDsr", login_required(views.AgentDSR), name="agentDsr"),
    path("dsrview", login_required(views.Dsrview), name="dsrview"),
    path("DSR", login_required(views.DSR), name="DSR"),
    path("liveStreaming", login_required(views.liveStreaming), name="liveStreaming"),
    path("createTask", login_required(views.createTask), name="createTask"),
    path("viewTask", login_required(views.viewTask), name="viewTask"),
    path("createDocument", login_required(views.createDocument), name="createDocument"),
    path("viewDocument", login_required(views.viewDocument), name="viewDocument"),
    path('validate-password/', views.validate_password_view, name='validate_password'),
    path("agentmeeting", login_required((views.AgentMeeting.as_view())), name="agentmeeting"),
    path("agentcalling", login_required((views.AgentCalling.as_view())), name="agentcalling"),
    path('view_calling/', views.ViewScheduledCalls.as_view(), name='view_calling'),
    path("view_meeting", login_required(views.ViewScheduledMeeting), name='view_meeting'),
    path("createNotes", login_required(views.createNotes), name='createNotes'),
    path("agentaccount", login_required(views.Agentaccount), name='agentaccount'),
    path("viewaccount", login_required(views.viewAccount), name='viewaccount'),
    path("viewcontact", login_required(views.viewcontact), name='viewcontact'),
    path("agentcalling", login_required((views.Schedule_Calling)), name="agentcalling"),
    path("leadImport", login_required((views.leadImport)), name="leadImport"),
    path("contactImport", login_required((views.contactImport)), name="contactImport"),
    path("quoteimport", login_required((views.quotesImport)), name="quoteimport"),
    path("opportunityimport", login_required((views.opportunityimport)), name="opportunityimport"),
    path("accountimport", login_required((views.accountimport)), name="accountimport"),
    path("DSRimport", login_required((views.DSRimport)), name="DSRimport"),
    path("miningimport", login_required((views.miningimport)), name="miningimport"),
    path("viewNotes", login_required((views.viewNotes)), name="viewNotes"),
    path('send-email/<int:meeting_id>/', views.send_meeting_email, name='send_meeting_email'),
    path("createInvoices", login_required((views.createInvoices)), name="createInvoices"),
    path("viewInvoices", login_required((views.viewInvoices)), name="viewInvoices"),
    path("viewemail", login_required((views.viewEmail)), name="viewemail"),
    path("agenttarget", login_required((views.Agenttarget)), name="agenttarget"),
    path("viewtarget", login_required((views.viewTarget)), name="viewtarget"),
    path("targetimport", login_required((views.Targetimport)), name="targetimport"),
    path("targetsList", login_required((views.TargetList)), name="targetsList"),
    path("viewtargetsList", login_required((views.viewTargetList)), name="viewtargetsList"),
    path("agentProjects", login_required((views.agentProjects)), name="agentProjects"),
    path("viewprojectList", login_required((views.viewProjectList)), name="viewprojectList"),
    path("projectimport", login_required((views.projectimport)), name="projectimport"),
    path("resourceCalendar", login_required((views.Resourcecalendar)), name="resourceCalendar"),
    path("viewprojectTask", login_required((views.ProjectTask)), name="viewprojectTask"),    
    path("Importtemplate", login_required((views.Templateimport)), name="Importtemplate"),
    path("createContract", login_required((views.createContract)), name="createContract"),
    path("viewContract", login_required((views.viewContract)), name="viewContract"),
    path("createManualTime", login_required((views.createManualTime)), name="createManualTime"),
    path("viewManualTime", login_required((views.viewManualTime)), name="viewManualTime"),
    path("viewprojectTask", login_required((views.ProjectTask)), name="viewprojectTask"),
    path("agentTemplate", login_required((views.agentTemplate)), name="agentTemplate"),
    path("viewTemplate", login_required((views.ViewTemplate)), name="viewTemplate"),
    path('Importtemplate/', views.upload_import_file, name='Importtemplate'),
    path('adminattendance', (views.AdminAttendence), name='adminattendance'),
    path("location", login_required((views.Location)), name="location"),
    path("createContract", login_required((views.create_contract)), name="createContract"),
    path("view_contract", login_required((views.view_contract)), name="viewContract"),
    path('createCase/', views.add_case, name='createCase'),
    path('viewCase/', views.view_cases, name='viewCase'),
    path("InvoiceImport", login_required((views.InvoiceImport)), name="InvoiceImport"),
    path('send-email-endpoint/', views.compose_email, name='send_email_endpoint'),
                
    path('agentemail', views.compose_email, name='agentemail'),
    path('inbox/', views.view_inbox, name='inbox/'),
    path('sent-emails/', views.view_sent_emails, name='sent-emails/'),

    path('createSurvey', views.survey_create, name='createSurvey'),
    path('surveydetail', views.survey_detail, name='surveydetail'),
    path('surveyview', views.survey_list, name='surveyview'),
    path('createKnowledgeBase', views.createKnowledgeBase, name='createKnowledgeBase'),
    path('viewKnowledgeBase', views.viewKnowledgeBase, name='viewKnowledgeBase'),
    




    # path('survey/<int:pk>/', views.survey_detail, name='survey_detail'),
    # path('surveys/', views.survey_list, name='survey_list'),
    # path("view_contact", login_required(views.ViewScheduledMeeting), name='view_contact'),  
    # path("agentcalling", login_required((views.schedule_calling_create)), name="agentcalling"),
    # path("viewemail", login_required(views.inbox), name="viewemail"),
    # Employee screen share URL
    # path('employee/screen-share/', views.employee_screen_share, name='employee_screen_share'),  
    # Admin screen view URL
    # path('screen-view/', views.admin_screen_view, name='admin_screen_view'),
    #path("createCase", login_required((views.createCase)), name="createCase"),
    # path("agentemail", login_required((views.compose_email)), name="agentemail"),
    # path("agentcalling", login_required((views.schedule_calling_create)), name="agentcalling"),
    # path('role-access/', views.role_access, name='role_access'),
    # path("agentcalling", login_required((views.AgentCalling.as_view())), name="agentcalling"),   
    # path("<int:user_id>/", login_required(views.Dashboards), name="Dashboards"),
    # path("adminn", login_required(views.Admin.as_view()), name="adminn"),
    # path("agent/", login_required(views.Agent.as_view()), name="agent"),
    
]
 

