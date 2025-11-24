from django.urls import path
from . import views

app_name = 'programs'

urlpatterns = [
    path('', views.ProgramListView.as_view(), name='list'),
    path('<uuid:pk>/', views.ProgramDetailView.as_view(), name='detail'),
]
