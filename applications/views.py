from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Application

from django.shortcuts import redirect
from django.contrib import messages

class ApplicationCreateView(LoginRequiredMixin, CreateView):
    model = Application
    fields = ['university', 'program', 'application_type', 'remarks']
    template_name = 'applications/create.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.documents.exists():
            messages.error(request, "You must upload at least one document (e.g., Passport, Transcript) before applying.")
            return redirect('students:upload_document')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('students:dashboard')

class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'applications/detail.html'
    context_object_name = 'application'
    
    def get_queryset(self):
        return Application.objects.filter(student=self.request.user).prefetch_related('logs')
