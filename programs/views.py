from django.views.generic import ListView, DetailView
from .models import Program

class ProgramListView(ListView):
    model = Program
    template_name = 'programs/program_list.html'
    context_object_name = 'programs'
    paginate_by = 20
    
    def get_queryset(self):
        return Program.objects.filter(is_active=True).select_related('university', 'type__level')

class ProgramDetailView(DetailView):
    model = Program
    template_name = 'programs/program_detail.html'
    context_object_name = 'program'
