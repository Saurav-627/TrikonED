from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'students'

urlpatterns = [
    path('login/', views.StudentLoginView.as_view(), name='login'),
    path('register/', views.StudentRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.StudentDashboardView.as_view(), name='dashboard'),
]
