from django.urls import path
from catalyst_app import views



urlpatterns = [
    path("", views.index,  name="index"),
    path("dashboard/", views.dashboard,  name="dashboard"),
    path("upload-csv/", views.csv_uploader,  name="upload-csv"),
    path("logout/", views.logout_view,  name="logout"),
    path('login/', views.sign_in, name='login'),
    path('register/', views.sign_up, name='register'),
    path('task-status/<task_id>/', views.task_status, name='task_status'),  # Task status polling endpoint

]