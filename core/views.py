from django.views.generic import TemplateView


class LandingPageView(TemplateView):
    """Landing page view"""
    template_name = 'core/landing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Import here to avoid circular imports
        from universities.models import University
        from programs.models import Program
        
        from students.models import Student
        from applications.models import Application
        
        context['featured_universities'] = University.objects.filter(
            is_partner=True
        ).select_related('location_emirate', 'contact_info')[:6]
        
        context['total_universities'] = University.objects.count()
        context['total_partner_universities'] = University.objects.filter(is_partner=True).count()
        context['total_programs'] = Program.objects.filter(is_active=True).count()
        context['total_student_help'] = Student.objects.count()
        
        # Success rate: Accepted / Total Applications
        total_apps = Application.objects.count()
        accepted_apps = Application.objects.filter(status='accepted').count()
        context['total_success_rate'] = int((accepted_apps / total_apps * 100)) if total_apps > 0 else 0
        
        return context


class AboutView(TemplateView):
    """About page view"""
    template_name = 'core/about.html'


class ContactView(TemplateView):
    """Contact page view"""
    template_name = 'core/contact.html'
