from django.views.generic import TemplateView, CreateView, UpdateView, FormView, ListView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Student, StudentDocument, StudentTestScore
from .forms import StudentRegisterForm, MultipleDocumentUploadForm, StudentProfileForm, StudentTestScoreForm

class StudentLoginView(LoginView):
    template_name = 'students/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('students:dashboard')

class StudentRegisterView(CreateView):
    model = Student
    form_class = StudentRegisterForm
    template_name = 'students/register.html'
    success_url = reverse_lazy('students:dashboard')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='core.backends.EmailOrUsernameModelBackend')
        return redirect(self.success_url)

class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'students/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from applications.models import Application
        from django.utils import timezone
        
        user_applications = Application.objects.filter(student=self.request.user).select_related('university', 'program').prefetch_related('logs')
        context['applications'] = user_applications
        context['pending_count'] = user_applications.filter(status='pending').count()
        context['documents'] = self.request.user.documents.all()
        
        # Get test scores and check for expired ones
        test_scores = self.request.user.test_scores.all()
        today = timezone.now().date()
        
        # Filter expired scores
        expired_scores = [score for score in test_scores if score.expiry_date and score.expiry_date < today]
        active_scores = [score for score in test_scores if not score.expiry_date or score.expiry_date >= today]
        
        context['test_scores'] = active_scores
        context['expired_test_scores'] = expired_scores
        
        # Check if profile is complete
        user = self.request.user
        profile_complete = all([
            user.first_name, user.last_name, user.phone, user.gender,
            user.nationality, user.date_of_birth, user.passport_number, user.passport_expiry
        ])
        context['profile_complete'] = profile_complete
        
        return context

class StudentProfileView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentProfileForm
    template_name = 'students/profile.html'
    success_url = reverse_lazy('students:dashboard')
    
    def get_object(self):
        return self.request.user

class StudentDocumentUploadView(LoginRequiredMixin, FormView):
    form_class = MultipleDocumentUploadForm
    template_name = 'students/document_upload.html'
    success_url = reverse_lazy('students:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student = self.request.user
        context['existing_passport'] = student.documents.filter(doc_type='passport').first()
        context['existing_transcript'] = student.documents.filter(doc_type='transcript').first()
        context['existing_other_documents'] = student.documents.filter(doc_type='other').order_by('-uploaded_at')
        return context

    def form_valid(self, form):
        student = self.request.user
        
        # Save/Replace Passport
        if 'passport' in form.cleaned_data and form.cleaned_data['passport']:
            passport_file = form.cleaned_data['passport']
            # Delete old passport if exists
            StudentDocument.objects.filter(student=student, doc_type='passport').delete()
            StudentDocument.objects.create(
                student=student,
                doc_type='passport',
                file_url=passport_file,
                file_name=passport_file.name
            )
        
        # Save/Replace Transcript
        if 'transcript' in form.cleaned_data and form.cleaned_data['transcript']:
            transcript_file = form.cleaned_data['transcript']
            # Delete old transcript if exists
            StudentDocument.objects.filter(student=student, doc_type='transcript').delete()
            StudentDocument.objects.create(
                student=student,
                doc_type='transcript',
                file_url=transcript_file,
                file_name=transcript_file.name
            )
        
        # Save Other Documents (append, don't replace)
        files = self.request.FILES.getlist('other_documents')
        for f in files:
            StudentDocument.objects.create(
                student=student,
                doc_type='other',
                file_url=f,
                file_name=f.name
            )
            
        return super().form_valid(form)


class TestScoreListView(LoginRequiredMixin, ListView):
    """View to list all test scores for the logged-in student"""
    model = StudentTestScore
    template_name = 'students/test_scores.html'
    context_object_name = 'object_list'
    
    def get_queryset(self):
        # Return all test scores (both active and expired)
        return StudentTestScore.objects.filter(
            student=self.request.user
        ).order_by('-test_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.utils import timezone
        context['today'] = timezone.now().date()
        return context


class TestScoreCreateView(LoginRequiredMixin, CreateView):
    """View to add a new test score"""
    model = StudentTestScore
    form_class = StudentTestScoreForm
    template_name = 'students/test_score_form.html'
    success_url = reverse_lazy('students:test_scores')
    
    def form_valid(self, form):
        form.instance.student = self.request.user
        messages.success(self.request, 'Test score added successfully!')
        return super().form_valid(form)


class TestScoreUpdateView(LoginRequiredMixin, UpdateView):
    """View to update an existing test score"""
    model = StudentTestScore
    form_class = StudentTestScoreForm
    template_name = 'students/test_score_form.html'
    success_url = reverse_lazy('students:test_scores')
    
    def get_queryset(self):
        return StudentTestScore.objects.filter(student=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Test score updated successfully!')
        return super().form_valid(form)


class TestScoreDeleteView(LoginRequiredMixin, DeleteView):
    """View to delete a test score"""
    model = StudentTestScore
    success_url = reverse_lazy('students:test_scores')
    
    def get_queryset(self):
        return StudentTestScore.objects.filter(student=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Test score deleted successfully!')
        return super().delete(request, *args, **kwargs)

