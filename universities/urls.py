from django.urls import path
from . import views

app_name = 'universities'

urlpatterns = [
    path('', views.UniversityListView.as_view(), name='list'),
    path('<uuid:pk>/', views.UniversityDetailView.as_view(), name='detail'),
]
