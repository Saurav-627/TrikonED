from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('create/', views.ApplicationCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.ApplicationDetailView.as_view(), name='detail'),
]
