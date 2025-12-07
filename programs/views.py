from django.views.generic import ListView, DetailView
from .models import Program

from django.contrib.auth.mixins import LoginRequiredMixin
from students.models import StudentUniversityVisit

class ProgramListView(ListView):
    model = Program
    template_name = 'programs/program_list.html'
    context_object_name = 'programs'
    paginate_by = 20
    
    def get_queryset(self):
        return Program.objects.filter(is_active=True).select_related('university', 'type__level')

class ProgramDetailView(LoginRequiredMixin, DetailView):
    model = Program
    template_name = 'programs/program_detail.html'
    context_object_name = 'program'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.utils import timezone
        context['next_intake'] = self.object.intakes.filter(
            start_date__gte=timezone.now().date()
        ).order_by('start_date').first()
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
