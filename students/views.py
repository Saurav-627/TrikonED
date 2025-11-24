from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Student

class StudentLoginView(LoginView):
    template_name = 'students/login.html'
    redirect_authenticated_user = True

class StudentRegisterView(CreateView):
    model = Student
    fields = ['username', 'email', 'password']
    template_name = 'students/register.html'
    success_url = reverse_lazy('students:login')
    
    def form_valid(self, form):
        # Hash the password properly
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'students/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from applications.models import Application
        context['applications'] = Application.objects.filter(student=self.request.user).select_related('university', 'program').prefetch_related('logs')
        context['documents'] = self.request.user.documents.all()
        return context

