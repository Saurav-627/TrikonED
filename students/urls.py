from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'students'

urlpatterns = [
    path('login/', views.StudentLoginView.as_view(), name='login'),
    path('register/', views.StudentRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.StudentDashboardView.as_view(), name='dashboard'),
    path('profile/', views.StudentProfileView.as_view(), name='profile'),
    path('documents/upload/', views.StudentDocumentUploadView.as_view(), name='upload_document'),
    
    # Test Score URLs
    path('test-scores/', views.TestScoreListView.as_view(), name='test_scores'),
    path('test-scores/add/', views.TestScoreCreateView.as_view(), name='add_test_score'),
    path('test-scores/<uuid:pk>/edit/', views.TestScoreUpdateView.as_view(), name='edit_test_score'),
    path('test-scores/<uuid:pk>/delete/', views.TestScoreDeleteView.as_view(), name='delete_test_score'),
]

