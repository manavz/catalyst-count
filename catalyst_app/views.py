import csv
import os

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.sessions.models import Session
from django.contrib.auth import logout
from django.contrib import messages
from catalyst_app.forms import RegisterForm, CSVUploadForm
from .tasks import process_csv
import pandas as pd
import io
import csv
from django.http import JsonResponse
from celery.result import AsyncResult
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib import messages

def task_status(request, task_id):
    task_result = AsyncResult(task_id)
    if task_result.state == 'PROGRESS':
        response = {
            'state': task_result.state,
            'current': task_result.info.get('current', 0),
            'total': task_result.info.get('total', 1),
        }
    else:
        response = {
            'state': task_result.state,
            'current': 0,
            'total': 1,
        }
    return JsonResponse(response)



def index(request):
    return render(request, 'login.html')


def count_rows_in_csv(csv_file_path):
    """Counts the total number of rows in the CSV file."""
    with open(csv_file_path, 'r') as file:
        reader = csv.reader(file)
        return sum(1 for row in reader)

def dashboard(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            form = CSVUploadForm()
            return render(request, 'home.html', {'form': form})

        if request.method == 'POST':
            form = CSVUploadForm(request.POST, request.FILES)
            if form.is_valid():
                csv_file = request.FILES['csv_file']

                print("======= 1 =========")
                # Check if the file is a CSV
                if not csv_file.name.endswith('.csv'):
                    messages.error(request, 'This is not a CSV file.')
                    return redirect('home')
                try:
                    print("======= 2 =========")
                    # Save the file to a temporary location
                    # file_name = default_storage.save(f'tmp/{csv_file.name}', csv_file)
                    # file_path = os.path.join(settings.MEDIA_ROOT, file_name)

                    chunk_size = 10000  # Number of rows per chunk
                    chunk = []
                    for i, line in enumerate(csv_file):
                        # Decode the byte stream into a string
                        decoded_line = line.decode('utf-8')
                        chunk.append(decoded_line)

                        # When chunk size is reached, send the chunk to Celery
                        if (i + 1) % chunk_size == 0:
                            print("======= 3 =========")

                            process_csv.delay(''.join(chunk))  # Join the chunk and send to Celery
                            chunk = []  # Reset the chunk

                        # Process any remaining rows that didn't complete a full chunk
                    if chunk:
                        process_csv.delay(''.join(chunk))

                except Exception as e:
                    messages.error(request, f'Error processing the CSV file: {e}')
                    return redirect('dashboard')

    return redirect('index')



def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to create the user
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, 'Registration failed. Please correct the errors.')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def sign_in(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = username
            request.session.save()
            return redirect('dashboard')
        else:
            messages.info(request, "invalid credentials")
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_view(request):
    logout(request)
    # clear the user's session data
    Session.objects.filter(session_key=request.session.session_key).delete()
    return redirect('login')


def csv_uploader(requset):
    if requset.method == 'POST':
        csv_file = requset.FILES['csv']
        csv_data = pd.read_csv(
            io.StringIO(
                csv_file.read().decode("utf-8")
            )
        )
        print("==== CSV DATA =====>", csv_data.head(10))

        for record in csv_data.to_dict(orient="records"):
            print("===== RECORD =====>", record)



