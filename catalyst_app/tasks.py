import csv
from celery import shared_task, current_task
from io import StringIO
from .models import CsvModel
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


@shared_task(bind=True)
def process_csv(self, chunk, total_rows):

    f = StringIO(chunk)
    reader = csv.reader(f)
    # print("======== READER =========", reader)
    self.update_state(state='PROGRESS', meta={'current': 0, 'total': total_rows})

    batch_create = []
    batch_update = []
    processed_rows = 0
    batch_size = 10000 

    # Process the CSV rows here
    for row in reader:
        
        if len(row) < 11:
            continue
        

        existing = CsvModel.objects.filter(domain=row[2]).first()
        if existing:
            # Update the existing record
            # print("======= EXISTING ROW ======>", row)
            existing.keyword = row[0]
            existing.name = row[1]
            existing.year_founded = row[3]
            existing.industry = row[4]
            existing.size_range = row[5]
            existing.locality = row[6]
            existing.country = row[7]
            existing.linkedin_url = row[8]
            existing.current_employee_estimate = row[9]
            existing.total_employee_estimate = row[10]
            batch_update.append(existing)
        else:
            # print("======= CREATING ROW ======>", row)
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
            batch_create.append(data)

        processed_rows += 1

        if len(batch_create) >= batch_size:
            CsvModel.objects.bulk_create(batch_create)
            batch_create = []

        if len(batch_update) >= batch_size:
            CsvModel.objects.bulk_update(batch_update, [
                    'keyword', 'name', 'year_founded', 'industry', 
                    'size_range', 'locality', 'country', 'linkedin_url', 
                    'current_employee_estimate', 'total_employee_estimate'
                ])
            batch_update = []


        # Periodic progress update
        if processed_rows % 1000 == 0:
            # self.update_state(state='PROGRESS', meta={'current': processed_rows, 'total': total_rows})
            if processed_rows % 1000 == 0:  # Update after every 1000 rows
                progress_percentage = (processed_rows / total_rows) * 100

                # Send progress to WebSocket
                async_to_sync(channel_layer.group_send)(
                    'progress_group',  # Group name
                    {
                        'type': 'send_progress_update',
                        'progress': progress_percentage
                    }
                )

        print({'processed_rows': processed_rows, 'total_rows': total_rows})
    
    return {'current': processed_rows, 'total': total_rows, 'status': 'Task completed!'}

