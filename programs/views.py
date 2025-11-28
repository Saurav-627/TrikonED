from django.views.generic import ListView, DetailView
from .models import Program

class ProgramListView(ListView):
    model = Program
    template_name = 'programs/program_list.html'
    context_object_name = 'programs'
    paginate_by = 20
    
    def get_queryset(self):
        return Program.objects.filter(is_active=True).select_related('university', 'type__level')

from django.contrib.auth.mixins import LoginRequiredMixin
from students.models import StudentUniversityVisit

class ProgramDetailView(LoginRequiredMixin, DetailView):
    model = Program
    template_name = 'programs/program_detail.html'
    context_object_name = 'program'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.user.is_authenticated:
            visit, created = StudentUniversityVisit.objects.get_or_create(
                student=request.user,
                university=self.object.university
            )
            if not created:
                visit.visit_count += 1
                visit.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
