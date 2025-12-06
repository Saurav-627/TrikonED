from django.urls import path
from . import views
from .application_form_views import ApplicationFormView

app_name = 'applications'

urlpatterns = [
    path('create/', views.ApplicationCreateView.as_view(), name='create'),  # Keep old for now
    path('apply/', ApplicationFormView.as_view(), name='apply'),  # New application form
    path('<str:application_id>/', views.ApplicationDetailView.as_view(), name='detail'),
    path('<str:application_id>/cancel/', views.ApplicationCancelView.as_view(), name='cancel'),
    path('<str:application_id>/pdf/', views.ApplicationPDFView.as_view(), name='pdf'),
]

