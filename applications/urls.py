from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('create/', views.ApplicationCreateView.as_view(), name='create'),
    path('<str:application_id>/', views.ApplicationDetailView.as_view(), name='detail'),
    path('<str:application_id>/cancel/', views.ApplicationCancelView.as_view(), name='cancel'),
]
