from django.views.generic import TemplateView


class LandingPageView(TemplateView):
    """Landing page view"""
    template_name = 'core/landing.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Import here to avoid circular imports
        from universities.models import University
        from programs.models import Program
        
        context['featured_universities'] = University.objects.filter(
            is_partner=True
        ).select_related('location_emirate', 'contact_info')[:6]
        context['total_universities'] = University.objects.count()
        context['total_programs'] = Program.objects.filter(is_active=True).count()
        return context


class AboutView(TemplateView):
    """About page view"""
    template_name = 'core/about.html'


class ContactView(TemplateView):
    """Contact page view"""
    template_name = 'core/contact.html'
