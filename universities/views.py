from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from students.models import StudentUniversityVisit
from .models import University
import string


class UniversityListView(ListView):
    """University listing with A-Z navigation and filters"""
    model = University
    template_name = 'universities/university_list.html'
    context_object_name = 'universities'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = University.objects.select_related('location_emirate', 'contact_info').prefetch_related('programs')
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Filter by emirate
        emirate = self.request.GET.get('emirate', '')
        if emirate:
            queryset = queryset.filter(location_emirate_id=emirate)
        
        # Filter by type
        uni_type = self.request.GET.get('type', '')
        if uni_type:
            queryset = queryset.filter(university_type=uni_type)
        
        # Filter by partner status
        partner = self.request.GET.get('partner', '')
        if partner:
            queryset = queryset.filter(is_partner=True)
        
        # A-Z filter
        letter = self.request.GET.get('letter', '')
        if letter:
            queryset = queryset.filter(name__istartswith=letter)
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from core.models import Emirate
        context['emirates'] = Emirate.objects.all()
        context['alphabet'] = string.ascii_uppercase
        context['current_letter'] = self.request.GET.get('letter', '')
        return context


from django.contrib.auth.mixins import LoginRequiredMixin
from students.models import StudentUniversityVisit

class UniversityDetailView(LoginRequiredMixin, DetailView):
    """University detail page"""
    model = University
    template_name = 'universities/university_detail.html'
    context_object_name = 'university'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated:
            # Check if this is a tab switch or reload
            # Only count if the user is NOT coming from the same page
            referer = request.META.get('HTTP_REFERER', '')
            current_path = request.path
            
            if not referer or current_path not in referer:
                visit, created = StudentUniversityVisit.objects.get_or_create(
                    student=request.user,
                    university=self.object
                )
                if not created:
                    visit.visit_count += 1
                    visit.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
    def get_queryset(self):
        return University.objects.select_related('location_emirate', 'contact_info').prefetch_related(
            'programs', 'programs__type', 'scholarships', 'accepted_curricula__curriculum',
            'enrollment_stats', 'visa_sponsorships'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the active tab from query params, default to 'overview'
        context['active_tab'] = self.request.GET.get('tab', 'overview')
        # Get latest enrollment stats
        context['latest_stats'] = self.object.enrollment_stats.first()
        # Get enrollment history for chart (last 4 years)
        context['enrollment_history'] = self.object.enrollment_stats.all()[:4]
        return context

