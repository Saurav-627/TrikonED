from django.views.generic import CreateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Application, ApplicationLog

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from .forms import ApplicationForm

class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'applications/create.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.documents.exists():
            messages.error(request, "You must upload at least one document (e.g., Passport, Transcript) before applying.")
            return redirect('students:upload_document')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        application = form.save(commit=False)
        application.status = 'pending'  # Set status to pending on submission
        application.save()
        
        # Create initial log entry
        ApplicationLog.objects.create(
            application=application,
            event='Application Submitted',
            details=f'Application submitted for {application.program.name} at {application.university.name}'
        )
        
        messages.success(self.request, 'Application submitted successfully!')
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('students:dashboard')

class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'applications/detail.html'
    context_object_name = 'application'
    slug_field = 'application_id'
    slug_url_kwarg = 'application_id'
    
    def get_queryset(self):
        return Application.objects.filter(student=self.request.user).prefetch_related('logs')

class ApplicationCancelView(LoginRequiredMixin, DeleteView):
    model = Application
    slug_field = 'application_id'
    slug_url_kwarg = 'application_id'
    
    def get_queryset(self):
        # Only allow canceling draft applications
        return Application.objects.filter(student=self.request.user, status='draft')
    
    def get_success_url(self):
        messages.success(self.request, 'Application cancelled successfully.')
        return reverse_lazy('students:dashboard')
    
    def get(self, request, *args, **kwargs):
        # Allow GET requests to delete (for simple links)
        return self.delete(request, *args, **kwargs)
