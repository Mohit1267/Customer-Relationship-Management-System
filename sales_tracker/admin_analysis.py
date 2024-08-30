import os
import sys
import numpy as np
import matplotlib.pyplot as plt
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, "..")
sys.path.append(project_directory)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stpa.settings'
from users.models import RegisterUser,AttendanceRecord, Profile, DaysStatus
from sales_tracker.models import MiningData,LeadsData
from django.db import connection
from django.utils import timezone
from datetime import timedelta

end_date = timezone.now().date()
start_date = end_date - timedelta(days=6)

# Query the data
week_attendance = AttendanceRecord.objects.filter(date__range=[start_date, end_date])


from collections import defaultdict

# Initialize dictionary to hold data
data = defaultdict(lambda: {'Present': 0, 'Absent': 0, 'Late': 0})

for record in week_attendance:
    date = record.date
    status = record.status
    data[date][status] += 1

# Convert the data into lists for plotting
dates = sorted(data.keys())
present_counts = [data[date]['Present'] for date in dates]
absent_counts = [data[date]['Absent'] for date in dates]
late_counts = [data[date]['Late'] for date in dates]  # New line for 'Late' status


x = np.arange(len(dates))
width = 0.25  # Width of the bars
def admin_attendence_graph():
    print("this is in admin attendece function")
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.gcf().set_facecolor('#262626')
    ax = plt.gca()
    ax.set_facecolor('#262626')

    
    ax.bar(x - width, present_counts, width, label='Present', color='#1f77b4')
    ax.bar(x, absent_counts, width, label='Absent', color='#ff7f0e')
    ax.bar(x + width, late_counts, width, label='Late', color='#2ca02c')

    # ax.bar(dates, present_counts, label='Present')
    # ax.bar(dates, absent_counts, bottom=present_counts, label='Absent')
    # ax.bar(dates, late_counts, bottom=[p + a for p, a in zip(present_counts, absent_counts)], label='Late')  # Stacked bar for 'Late'

    ax.set_xlabel('Date')
    ax.set_ylabel('Total Number of Employees')
    ax.set_title('Employee Attendance for Initial 7 Days')
    ax.set_xticks(x)
    ax.set_xticklabels([date.strftime('%Y-%m-%d') for date in dates], rotation=45)
    ax.legend(title='Status')
    # ax.set_xticklabels(dates, rotation=45)
    plt.tight_layout()
    plt.savefig('static/admin_attendence.png', bbox_inches='tight', facecolor='#262626')
    



attendence_percentage = []
late = []
a = RegisterUser.objects.count()
Total_att = a*7

TWend_date = timezone.now().date()
TWstart_date = TWend_date - timedelta(days=6)
OWend_date = timezone.now().date() - timedelta(days=6) 
OWstart_date = TWend_date - timedelta(days=12)
def Att_perct():
    TWattendance = AttendanceRecord.objects.filter(date__range=[TWstart_date, TWend_date],status__in=['Present', 'Late']).count()

    OWattendance = AttendanceRecord.objects.filter(date__range=[OWstart_date, OWend_date],status__in=['Present', 'Late']).count()
    attendence_percentage.append((OWattendance/Total_att)*100)
    attendence_percentage.append((TWattendance/Total_att)*100)
    perct_change = ((attendence_percentage[1]- attendence_percentage[0])/attendence_percentage[0])*100

    print(attendence_percentage)
    print(perct_change)
    return perct_change

def Late_perct():
    TWlate= AttendanceRecord.objects.filter(date__range=[TWstart_date, TWend_date],status__in=['Late']).count()
    OWLate = AttendanceRecord.objects.filter(date__range=[OWstart_date, OWend_date],status__in=['Late']).count()
    late.append((OWLate/Total_att)*100)
    late.append((TWlate/Total_att)*100)
    perct_changeLate = ((late[1]- attendence_percentage[0])/late[0])*100
    return perct_changeLate 
    print(late)
    print(perct_changeLate)








def Mining_Count():
    Total_Mining = MiningData.objects.count()
    Exp_M = AttendanceRecord.objects.values('date').distinct().count()
    MinerC = Profile.objects.filter(branch = "miner").count()
    Exp_Mining = Exp_M*MinerC*40

    # Data
    labels = ['Total Mining', 'Expected Mining']
    sizes = [Total_Mining, Exp_Mining]
    colors = ['#ff9999','#66b3ff']

    # Plot
    fig, ax = plt.subplots(figsize=(4.5, 4), subplot_kw=dict(aspect="equal"))
    plt.gcf().set_facecolor('#262626')
    ax.set_facecolor('#262626')

    # Create a pie chart
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.4),textprops=dict(color='white'))

    # Beautify the plot
    plt.setp(autotexts, size=10, weight="bold",)
    plt.setp(texts, size=12, color='white')
    ax.set_title("Mining vs Expected Mining", color='white')

    # Show plot
    plt.savefig('static/Mining_Count.png')

def Leads_Count():
    Total_Leads = LeadsData.objects.count()
    Exp_L = AttendanceRecord.objects.values('date').distinct().count()
    AgentC = Profile.objects.filter(branch = "agent").count()
    Exp_Leads = Exp_L*AgentC*4

    # Data
    labels = ['Total Mining', 'Expected Mining']
    sizes = [Total_Leads, Exp_Leads]
    colors = ['#ff9999','#66b3ff']

    # Plot
    fig, ax = plt.subplots(figsize=(4.5, 4), subplot_kw=dict(aspect="equal"))
    plt.gcf().set_facecolor('#262626')
    ax.set_facecolor('#262626')

    # Create a pie chart
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.4),textprops=dict(color='white'))

    # Beautify the plot
    plt.setp(autotexts, size=10, weight="bold",)
    plt.setp(texts, size=12, color='white')
    ax.set_title("Leads vs Expected Leads", color='white')

    # Show plot
    plt.savefig('static/Leads_Count.png')




def EachMinerTarget(id):
    with connection.cursor() as cursor:
        cursor.execute("""
        select A.status, COUNT(*) as count 
        from users_attendancerecord as A
        left join users_daysstatus as D
        ON D.date = A.date
        where A.user_id = %s and D.status = 'Working Day'
        group by A.status;
        """,[id])
        data = cursor.fetchall()
        print(data) 
        target = sum(row[1] for row in data)*40
        print(target)
    acchieved = MiningData.objects.filter(created_by_id = id).count()
    print(acchieved) 
    each_miner = {"Target":target, "Acchieve":acchieved}
    labels = [f'target:{target}', f'acchieved:{acchieved}']
    sizes = [target, acchieved]
    colors = ['#ff9999','#66b3ff']

    # Plot
    fig, ax = plt.subplots(figsize=(4.5, 4), subplot_kw=dict(aspect="equal"))
    plt.gcf().set_facecolor('#262626')
    ax.set_facecolor('#262626')

    # Create a pie chart
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, wedgeprops=dict(width=0.4),textprops=dict(color='white'))

    # Beautify the plot
    plt.setp(autotexts, size=10, weight="bold",)
    plt.setp(texts, size=12, color='white')
    ax.set_title("Mining vs Expected Mining", color='white')

    # Show plot
    plt.savefig('static/EachMinerTarget.png')

    return each_miner 
    # wd = DaysStatus.objects.filter(status='Working Day')
    # attendence = AttendanceRecord.objects.filter(user_id = id)
    # print(attendence)


def Time_worked():
    with connection.cursor() as cursor:
        cursor.execute("""
        SELECT 
        A.date,
        SUM(TIMESTAMPDIFF(
            SECOND, 
            CONCAT(A.date, ' ', A.check_in_time), 
            IFNULL(CONCAT(A.date, ' ', A.check_out_time), NOW())
        ))
        AS time_worked
        FROM 
        users_attendancerecord as A
        left join users_daysstatus as D
        on A.date = D.date
        where D.status = 'Working Day'
        group by A.date;
        """)
        data = cursor.fetchall()
        dates = []
        hours_worked = []
        for row in data:
            date,total_sec = row
            hours = total_sec / 3600
            dates.append(date)
            hours_worked.append(hours)
            print(date,hours)
            print(' ')
            
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Set face color
        plt.gcf().set_facecolor('#262626')
        ax.set_facecolor('#262626')
        
        # Plotting the line graph
        ax.plot(dates, hours_worked, marker='o', linestyle='-', color='b')
        ax.set_xlabel('Date', color='white')
        ax.set_ylabel('Hours Worked', color='white')
        ax.set_title('Hours Worked vs. Date', color='white')
        
        # Beautify the plot
        plt.xticks(rotation=45, color='white')
        plt.yticks(color='white')
        plt.tight_layout()
        plt.savefig('static/Time_worked.png')