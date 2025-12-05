from django.urls import path
from . import views
from .wizard_views import ApplicationWizardView

app_name = 'applications'

urlpatterns = [
    path('create/', views.ApplicationCreateView.as_view(), name='create'),  # Keep old for now
    path('wizard/', ApplicationWizardView.as_view(), name='wizard'),  # New wizard
    path('<str:application_id>/', views.ApplicationDetailView.as_view(), name='detail'),
    path('<str:application_id>/cancel/', views.ApplicationCancelView.as_view(), name='cancel'),
    path('<str:application_id>/pdf/', views.ApplicationPDFView.as_view(), name='pdf'),
]

