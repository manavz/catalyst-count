import csv
from celery import shared_task
from io import StringIO
from .models import CsvModel


@shared_task()
def process_csv(chunk):
    print("======= 4 =========")

    f = StringIO(chunk)
    reader = csv.reader(f)

    # self.update_state(state='PROGRESS', meta={'current': 0, 'total': total_rows})

    processed_rows = 0
    # Process the CSV rows here
    for i, row in enumerate(reader):
        # Example: Print each row (replace with actual processing logic)
        print("======= ROW ======>", row)
        data = CsvModel()
        data.keyword = row[0]
        data.name = row[1]
        data.domain = row[2]
        data.year_founded = row[3]
        data.industry = row[4]
        data.size_range = row[5]
        data.locality = row[6]
        data.country = row[7]
        data.linkedin_url = row[8]
        data.current_employee_estimate = row[9]
        data.total_employee_estimate = row[10]
        data.save()
        processed_rows += i

        # Update progress
        # self.update_state(state='PROGRESS', meta={'current': processed_rows, 'total': total_rows})
    print("====== PROCESSED ROWS =======>", processed_rows)
    return 'csv DATA Uploaded Successfuly'

