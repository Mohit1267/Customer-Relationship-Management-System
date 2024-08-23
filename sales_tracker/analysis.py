import os
import sys
import django
current_directory = os.path.dirname(os.path.abspath(__file__))
project_directory = os.path.join(current_directory, "..")
sys.path.append(project_directory)
os.environ['DJANGO_SETTINGS_MODULE'] = 'stpa.settings'
from django.db import connection
import matplotlib.pyplot as plt
def fetch_records():
    with connection.cursor() as cursor:
        # Execute a raw SQL query to fetch records data
        cursor.execute("select * from users_attendancerecord")
        # Fetch all rows from the result set
        records = cursor.fetchall()
        print(type(records))
        # print(records)

        # Process the records data
        for record in records:
            print(record)


def generate_bar_chart():
    with connection.cursor() as cursor:
        cursor.execute("SELECT category, COUNT(*) FROM website_records GROUP BY category")
        data = cursor.fetchall()

        categories, counts = zip(*data)

        # Create a bar chart using Matplotlib
        plt.bar(categories, counts)
        plt.xlabel('Category')
        plt.ylabel('Count')
        plt.title('Record Count by Category')
        plt.savefig('path/to/static/images/bar_chart.png')