# dwitter/urls.py

from django.urls import path
from .views import dashboard, profile_list, profile, SignupPage, LoginPage, edit_dweet, delete_dweet

app_name = "dwitter"

urlpatterns = [
    path('',SignupPage,name='signup'),
    path('login/',LoginPage,name='login'),
    path("dashboard/", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:pk>/", profile, name="profile"),
    path('edit_dweet/<int:dweet_id>/', edit_dweet, name='edit_dweet'),
    path('delete_dweet/<int:dweet_id>/', delete_dweet, name='delete_dweet'),
]