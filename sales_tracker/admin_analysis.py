import os
import sys
import matplotlib.pyplot as plt
from users.models import RegisterUser,Profile,AttendanceRecord
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, "..")
sys.path.append(project_directory)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stpa.settings'
from django.db import connection
from django.utils import timezone
from datetime import timedelta

end_date = timezone.now().date()
start_date = end_date - timedelta(days=6)

# Query the data
week_attendance = AttendanceRecord.objects.filter(date__range=[start_date, end_date])


from collections import defaultdict

# Initialize dictionary to hold data
data = defaultdict(lambda: {'Present': 0, 'Absent': 0})

for record in week_attendance:
    date = record.date
    status = record.status
    data[date][status] += 1

# Convert the data into lists for plotting
dates = sorted(data.keys())
present_counts = [data[date]['Present'] for date in dates]
absent_counts = [data[date]['Absent'] for date in dates]


import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse

def admin_attendence_graph():
    fig, ax = plt.subplots(figsize=(12, 6))
    plt.gcf().set_facecolor('#262626')
    ax = plt.gca()
    ax.set_facecolor('#262626')
    ax.bar(dates, present_counts, label='Present')
    ax.bar(dates, absent_counts, bottom=present_counts, label='Absent')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Number of Employees')
    ax.set_title('Employee Attendance for Initial 7 Days')
    ax.legend(title='Status')
    ax.set_xticklabels(dates, rotation=45)

    # Save the plot to a BytesIO object
    # buf = BytesIO()
    # plt.savefig(buf, format='png')
    # buf.seek(0)
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



    
