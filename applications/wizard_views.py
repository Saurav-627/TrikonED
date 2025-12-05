"""
Multi-Step Application Wizard View
Handles 3-step application process:
1. Personal Information & Program Selection
2. Document Upload (optional)
3. English Proficiency (conditional - only if program requires it)
"""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Application, ApplicationLog
from .forms import ApplicationStep1Form, ApplicationStep2Form, ApplicationStep3Form
from students.models import StudentDocument, StudentTestScore
from programs.models import Program


class ApplicationWizardView(LoginRequiredMixin, TemplateView):
    """Multi-step application wizard"""
    template_name = 'applications/wizard.html'
    
    def get_current_step(self):
        """Get current step from session"""
        return self.request.session.get('application_wizard_step', 1)
    
    def set_current_step(self, step):
        """Set current step in session"""
        self.request.session['application_wizard_step'] = step
    
    def get_wizard_data(self, step=None):
        """Get wizard data from session"""
        if step:
            return self.request.session.get(f'application_wizard_step{step}_data', {})
        return {
            'step1': self.request.session.get('application_wizard_step1_data', {}),
            'step2': self.request.session.get('application_wizard_step2_data', {}),
            'step3': self.request.session.get('application_wizard_step3_data', {}),
        }
    
    def save_wizard_data(self, step, data):
        """Save wizard data to session"""
        self.request.session[f'application_wizard_step{step}_data'] = data
    
    def clear_wizard_data(self):
        """Clear all wizard data from session"""
        keys_to_delete = [
            'application_wizard_step',
            'application_wizard_step1_data',
            'application_wizard_step2_data',
            'application_wizard_step3_data',
        ]
        for key in keys_to_delete:
            if key in self.request.session:
                del self.request.session[key]
    
    def program_requires_english(self, program_id):
        """Check if program requires English proficiency"""
        try:
            program = Program.objects.get(pk=program_id)
            return program.english_requirements.exists()
        except Program.DoesNotExist:
            return False
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_step = self.get_current_step()
        
        # Check if this is a new application (different program/university in URL)
        if 'program' in self.request.GET or 'university' in self.request.GET:
            step1_data = self.get_wizard_data(1)
            
            # If we have existing wizard data, check if it's for a different program
            if step1_data:
                program_slug = self.request.GET.get('program')
                university_slug = self.request.GET.get('university')
                
                # Get the stored program/university IDs
                stored_program_id = step1_data.get('program')
                stored_university_id = step1_data.get('university')
                
                # Check if the URL params are different from stored data
                if program_slug or university_slug:
                    try:
                        if program_slug:
                            program = Program.objects.get(slug=program_slug)
                            if str(program.id) != str(stored_program_id):
                                # Different program - clear wizard
                                self.clear_wizard_data()
                                current_step = 1
                                self.set_current_step(1)
                        
                        if university_slug:
                            from universities.models import University
                            university = University.objects.get(slug=university_slug)
                            if str(university.id) != str(stored_university_id):
                                # Different university - clear wizard
                                self.clear_wizard_data()
                                current_step = 1
                                self.set_current_step(1)
                    except:
                        pass
        
        context['current_step'] = current_step
        context['total_steps'] = 3  # May be 2 if English not required
        
        # Get existing documents for Step 2
        if current_step == 2:
            context['existing_passport'] = self.request.user.documents.filter(doc_type='passport').first()
            context['existing_transcript'] = self.request.user.documents.filter(doc_type='transcript').first()
            context['existing_other_documents'] = self.request.user.documents.filter(doc_type='other')
        
        # Check if Step 3 is needed
        step1_data = self.get_wizard_data(1)
        if step1_data and 'program' in step1_data:
            context['english_required'] = self.program_requires_english(step1_data['program'])
        else:
            context['english_required'] = False
        
        # Get form for current step
        if current_step == 1:
            # Check for initial data from URL (program page)
            initial = {}
            if 'program' in self.request.GET:
                program_slug = self.request.GET.get('program')
                try:
                    # Try to get program by slug
                    program = Program.objects.get(slug=program_slug)
                    initial['program'] = program.id
                except Program.DoesNotExist:
                    pass
            if 'university' in self.request.GET:
                university_slug = self.request.GET.get('university')
                try:
                    # Try to get university by slug
                    from universities.models import University
                    university = University.objects.get(slug=university_slug)
                    initial['university'] = university.id
                except:
                    pass
            
            context['form'] = ApplicationStep1Form(
                initial=initial,
                user=self.request.user
            )
        elif current_step == 2:
            context['form'] = ApplicationStep2Form()
        elif current_step == 3:
            context['form'] = ApplicationStep3Form(user=self.request.user)
        
        return context
    
    def post(self, request, *args, **kwargs):
        current_step = self.get_current_step()
        action = request.POST.get('action', 'next')
        
        if action == 'prev':
            # Go to previous step
            if current_step > 1:
                self.set_current_step(current_step - 1)
            return redirect('applications:wizard')
        
        # Validate current step
        if current_step == 1:
            form = ApplicationStep1Form(request.POST, user=request.user)
            if form.is_valid():
                # Save step 1 data
                data = form.cleaned_data.copy()
                # Convert model instances to IDs for session storage
                if 'university' in data:
                    data['university'] = str(data['university'].id)
                if 'program' in data:
                    data['program'] = str(data['program'].id)
                # Convert date objects to strings for JSON serialization
                if 'date_of_birth' in data and data['date_of_birth']:
                    data['date_of_birth'] = data['date_of_birth'].isoformat()
                if 'passport_expiry' in data and data['passport_expiry']:
                    data['passport_expiry'] = data['passport_expiry'].isoformat()
                
                self.save_wizard_data(1, data)
                
                # Update student profile if needed
                student = request.user
                if not student.phone:
                    student.phone = form.cleaned_data['phone']
                if not student.gender:
                    student.gender = form.cleaned_data['gender']
                if not student.nationality:
                    student.nationality = form.cleaned_data['nationality']
                if not student.date_of_birth:
                    student.date_of_birth = form.cleaned_data['date_of_birth']
                if not student.passport_number:
                    student.passport_number = form.cleaned_data['passport_number']
                if not student.passport_expiry:
                    student.passport_expiry = form.cleaned_data['passport_expiry']
                if not student.address:
                    student.address = form.cleaned_data['address']
                student.save()
                
                # Move to step 2
                self.set_current_step(2)
                return redirect('applications:wizard')
            else:
                # Re-render with errors
                context = self.get_context_data()
                context['form'] = form
                return self.render_to_response(context)
        
        elif current_step == 2:
            form = ApplicationStep2Form(request.POST, request.FILES)
            if form.is_valid():
                # Save documents
                student = request.user
                
                if form.cleaned_data.get('passport'):
                    # Delete old passport
                    StudentDocument.objects.filter(student=student, doc_type='passport').delete()
                    StudentDocument.objects.create(
                        student=student,
                        doc_type='passport',
                        file_url=form.cleaned_data['passport'],
                        file_name=form.cleaned_data['passport'].name
                    )
                
                if form.cleaned_data.get('transcript'):
                    # Delete old transcript
                    StudentDocument.objects.filter(student=student, doc_type='transcript').delete()
                    StudentDocument.objects.create(
                        student=student,
                        doc_type='transcript',
                        file_url=form.cleaned_data['transcript'],
                        file_name=form.cleaned_data['transcript'].name
                    )
                
                # Handle multiple other documents
                files = request.FILES.getlist('other_documents')
                for f in files:
                    StudentDocument.objects.create(
                        student=student,
                        doc_type='other',
                        file_url=f,
                        file_name=f.name
                    )
                
                # Check if Step 3 is needed
                step1_data = self.get_wizard_data(1)
                if self.program_requires_english(step1_data.get('program')):
                    self.set_current_step(3)
                    return redirect('applications:wizard')
                else:
                    # Skip to submission
                    return self.submit_application(request)
            else:
                context = self.get_context_data()
                context['form'] = form
                return self.render_to_response(context)
        
        elif current_step == 3:
            form = ApplicationStep3Form(request.POST, user=request.user)
            if form.is_valid():
                data = form.cleaned_data
                
                # Save English proficiency if entered
                if data.get('use_existing_score') and data.get('existing_score'):
                    # Using existing score - just reference it
                    self.save_wizard_data(3, {'existing_score_id': str(data['existing_score'].id)})
                elif data.get('test_type') and data.get('test_date'):
                    # New score entered - save to student profile
                    score = StudentTestScore.objects.create(
                        student=request.user,
                        test_type=data['test_type'],
                        test_date=data['test_date'],
                        listening_score=data.get('listening_score'),
                        reading_score=data.get('reading_score'),
                        speaking_score=data.get('speaking_score'),
                        writing_score=data.get('writing_score'),
                        overall_score=data.get('overall_score'),
                    )
                    self.save_wizard_data(3, {'new_score_id': str(score.id)})
                
                # Submit application
                return self.submit_application(request)
            else:
                context = self.get_context_data()
                context['form'] = form
                return self.render_to_response(context)
        
        return redirect('applications:wizard')
    
    def submit_application(self, request):
        """Final submission of application"""
        step1_data = self.get_wizard_data(1)
        
        # Create application
        from programs.models import Program
        from universities.models import University
        
        program = Program.objects.get(pk=step1_data['program'])
        university = University.objects.get(pk=step1_data['university'])
        
        application = Application.objects.create(
            student=request.user,
            university=university,
            program=program,
            application_type=step1_data['application_type'],
            remarks=step1_data.get('remarks', ''),
            status='pending'
        )
        
        # Calculate lead quality
        has_documents = request.user.documents.exists()
        has_english = False
        if self.program_requires_english(step1_data['program']):
            step3_data = self.get_wizard_data(3)
            has_english = bool(step3_data)
        
        # Determine lead quality
        if has_documents and (has_english or not self.program_requires_english(step1_data['program'])):
            application.lead_quality = 'high'
        elif has_documents or has_english:
            application.lead_quality = 'medium'
        else:
            application.lead_quality = 'low'
        
        application.save()
        
        # Create log entry
        ApplicationLog.objects.create(
            application=application,
            event='Application Submitted',
            details=f'Application submitted for {program.name} at {university.name}'
        )
        
        # Clear wizard data
        self.clear_wizard_data()
        
        messages.success(request, 'Application submitted successfully!')
        return redirect('students:dashboard')
