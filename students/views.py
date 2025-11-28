from django.views.generic import TemplateView, CreateView, UpdateView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Student, StudentDocument
from .forms import StudentRegisterForm, MultipleDocumentUploadForm

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
        login(self.request, user)
        return super().form_valid(form)

class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'students/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from applications.models import Application
        user_applications = Application.objects.filter(student=self.request.user).select_related('university', 'program').prefetch_related('logs')
        context['applications'] = user_applications
        context['pending_count'] = user_applications.filter(status='pending').count()
        context['documents'] = self.request.user.documents.all()
        return context

class StudentDocumentUploadView(LoginRequiredMixin, FormView):
    form_class = MultipleDocumentUploadForm
    template_name = 'students/document_upload.html'
    success_url = reverse_lazy('students:dashboard')

    def form_valid(self, form):
        student = self.request.user
        
        # Save Passport
        passport_file = form.cleaned_data['passport']
        StudentDocument.objects.create(
            student=student,
            doc_type='passport',
            file_url=passport_file,
            file_name=passport_file.name
        )
        
        # Save Transcript
        transcript_file = form.cleaned_data['transcript']
        StudentDocument.objects.create(
            student=student,
            doc_type='transcript',
            file_url=transcript_file,
            file_name=transcript_file.name
        )
        
        # Save Other Documents
        files = self.request.FILES.getlist('other_documents')
        for f in files:
            StudentDocument.objects.create(
                student=student,
                doc_type='other',
                file_url=f,
                file_name=f.name
            )
            
        return super().form_valid(form)
