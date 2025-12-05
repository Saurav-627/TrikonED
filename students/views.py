from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Student, StudentDocument
from .forms import StudentRegisterForm, MultipleDocumentUploadForm, StudentProfileForm

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
        user_applications = Application.objects.filter(student=self.request.user).select_related('university', 'program').prefetch_related('logs')
        context['applications'] = user_applications
        context['pending_count'] = user_applications.filter(status='pending').count()
        context['documents'] = self.request.user.documents.all()
        
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
