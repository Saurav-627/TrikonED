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
        from django.db.models import Q
        from core.models import Country, Emirate
        
        queryset = University.objects.select_related('location_emirate', 'location_emirate__country', 'country', 'contact_info').prefetch_related('programs')
        
        # Search
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Filter by country - convert name to ID for filtering
        country_name = self.request.GET.get('country', '')
        if country_name:
            try:
                country = Country.objects.get(name__iexact=country_name)
                queryset = queryset.filter(
                    Q(location_emirate__country_id=country.id) | Q(country_id=country.id)
                )
            except Country.DoesNotExist:
                queryset = queryset.none()
        
        # Filter by emirate - convert name to ID for filtering
        emirate_name = self.request.GET.get('emirate', '')
        if emirate_name:
            try:
                emirate = Emirate.objects.get(name__iexact=emirate_name)
                queryset = queryset.filter(location_emirate_id=emirate.id)
            except Emirate.DoesNotExist:
                queryset = queryset.none()
        
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
        from core.models import Emirate, Country
        
        # Get all countries and emirates
        context['countries'] = Country.objects.all()
        context['emirates'] = Emirate.objects.select_related('country').all()
        
        # Get selected country name from URL
        selected_country_name = self.request.GET.get('country', '')
        context['selected_country'] = selected_country_name
        
        # Filter emirates by selected country (convert name to ID)
        if selected_country_name:
            try:
                country = Country.objects.get(name__iexact=selected_country_name)
                context['filtered_emirates'] = Emirate.objects.filter(country_id=country.id)
            except Country.DoesNotExist:
                context['filtered_emirates'] = Emirate.objects.none()
        else:
            context['filtered_emirates'] = Emirate.objects.none()
        
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
        
        # Program level filtering
        if context['active_tab'] == 'programs':
            from programs.models import ProgramLevel
            
            # Get all available program levels for this university
            available_levels = ProgramLevel.objects.filter(
                program_types__programs__university=self.object,
                program_types__programs__is_active=True
            ).distinct().order_by('name')
            context['available_levels'] = available_levels
            
            # Get selected level from query params
            selected_level = self.request.GET.get('level', '')
            context['selected_level'] = selected_level
            
            # Filter programs by level if selected
            if selected_level:
                context['filtered_programs'] = self.object.programs.filter(
                    type__level__name__iexact=selected_level,
                    is_active=True
                ).select_related('type', 'type__level')
            else:
                context['filtered_programs'] = self.object.programs.filter(
                    is_active=True
                ).select_related('type', 'type__level')
        
        return context

