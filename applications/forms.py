from django import forms
from .models import Application
from students.models import Student, StudentTestScore

from programs.models import Program

class ApplicationForm(forms.ModelForm):
    # Student fields
    phone = forms.CharField(required=True, label="Phone Number")
    gender = forms.ChoiceField(choices=Student._meta.get_field('gender').choices, required=True)
    nationality = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    passport_number = forms.CharField(required=True)
    passport_expiry = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)

    # Read-only level field
    level = forms.CharField(required=False, label="Program Level", widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Application
        fields = ['university', 'program', 'application_type', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
            'application_type': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Check if this is coming from a program page (has initial values from URL)
        from_program_page = bool(self.initial.get('program') and self.initial.get('university'))
        
        # Make personal info read-only ONLY if already populated
        personal_fields = ['phone', 'nationality', 'date_of_birth', 'passport_number', 'passport_expiry', 'address']
        for field in personal_fields:
            user_value = getattr(self.user, field, None)
            if user_value:
                self.fields[field].widget.attrs['readonly'] = True
                self.fields[field].widget.attrs['class'] = 'bg-gray-100 cursor-not-allowed w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] text-[#8d7a5e]'
            else:
                self.fields[field].widget.attrs['class'] = 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'

        # Handle gender separately (Select field)
        if self.user.gender:
            self.fields['gender'].widget.attrs['style'] = 'pointer-events: none; background-color: #f3f4f6;'
            self.fields['gender'].widget.attrs['readonly'] = True
            self.fields['gender'].widget.attrs['class'] = 'bg-gray-100 cursor-not-allowed w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] text-[#8d7a5e]'
        else:
            self.fields['gender'].widget.attrs['class'] = 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'
        
        # Filter programs based on university
        if 'university' in self.data:
            try:
                university_id = int(self.data.get('university'))
                self.fields['program'].queryset = Program.objects.filter(university_id=university_id)
            except (ValueError, TypeError):
                pass
        elif self.initial.get('university'):
            self.fields['program'].queryset = Program.objects.filter(university_id=self.initial['university'])
            # Only disable if coming from program page
            if from_program_page:
                self.fields['university'].widget.attrs['style'] = 'pointer-events: none; background-color: #f3f4f6;'
                self.fields['university'].widget.attrs['readonly'] = True
        else:
            self.fields['program'].queryset = Program.objects.none()

        # Handle Program and Level
        selected_program = None
        if 'program' in self.data:
            try:
                selected_program = Program.objects.get(pk=self.data.get('program'))
            except (ValueError, TypeError, Program.DoesNotExist):
                pass
        elif self.initial.get('program'):
            try:
                selected_program = Program.objects.get(pk=self.initial['program'])
                # Only disable if coming from program page
                if from_program_page:
                    self.fields['program'].widget.attrs['style'] = 'pointer-events: none; background-color: #f3f4f6;'
                    self.fields['program'].widget.attrs['readonly'] = True
            except Program.DoesNotExist:
                pass
        
        if selected_program:
            self.fields['level'].initial = selected_program.type.level.name
            # Auto-set application type based on level
            level_name = selected_program.type.level.name.lower()
            if 'bachelor' in level_name:
                self.fields['application_type'].initial = 'undergraduate'
            elif 'master' in level_name or 'phd' in level_name:
                self.fields['application_type'].initial = 'postgraduate'
            else:
                self.fields['application_type'].initial = 'diploma'

        if self.user:
            # Pre-fill student fields
            self.fields['phone'].initial = self.user.phone
            self.fields['gender'].initial = self.user.gender
            self.fields['nationality'].initial = self.user.nationality
            self.fields['date_of_birth'].initial = self.user.date_of_birth
            self.fields['passport_number'].initial = self.user.passport_number
            self.fields['passport_expiry'].initial = self.user.passport_expiry
            self.fields['address'].initial = self.user.address

    def save(self, commit=True):
        application = super().save(commit=False)
        if self.user:
            # Update student profile
            # Update student profile - only update empty fields
            student = self.user
            if not student.phone:
                student.phone = self.cleaned_data['phone']
            if not student.gender:
                student.gender = self.cleaned_data['gender']
            if not student.nationality:
                student.nationality = self.cleaned_data['nationality']
            if not student.date_of_birth:
                student.date_of_birth = self.cleaned_data['date_of_birth']
            if not student.passport_number:
                student.passport_number = self.cleaned_data['passport_number']
            if not student.passport_expiry:
                student.passport_expiry = self.cleaned_data['passport_expiry']
            if not student.address:
                student.address = self.cleaned_data['address']
            student.save()
            
            application.student = student
        
        if commit:
            application.save()
        return application


# ============================================
# Multi-Step Application Wizard Forms
# ============================================

class ApplicationStep1Form(forms.ModelForm):
    """Step 1: Personal Information & Program Selection"""
    # Student fields
    phone = forms.CharField(required=True, label="Phone Number")
    gender = forms.ChoiceField(choices=Student._meta.get_field('gender').choices, required=True)
    nationality = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    passport_number = forms.CharField(required=True)
    passport_expiry = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    level = forms.CharField(required=False, label="Program Level", widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Application
        fields = ['university', 'program', 'application_type', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
            'application_type': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        from_program_page = bool(self.initial.get('program') and self.initial.get('university'))
        
        # Make personal info read-only if already populated
        personal_fields = ['phone', 'nationality', 'date_of_birth', 'passport_number', 'passport_expiry', 'address']
        for field in personal_fields:
            user_value = getattr(self.user, field, None)
            if user_value:
                self.fields[field].widget.attrs['readonly'] = True
                self.fields[field].widget.attrs['class'] = 'bg-gray-100 cursor-not-allowed w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] text-[#8d7a5e]'
            else:
                self.fields[field].widget.attrs['class'] = 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'

        if self.user and self.user.gender:
            self.fields['gender'].widget.attrs['style'] = 'pointer-events: none; background-color: #f3f4f6;'
            self.fields['gender'].widget.attrs['readonly'] = True
            self.fields['gender'].widget.attrs['class'] = 'bg-gray-100 cursor-not-allowed w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] text-[#8d7a5e]'
        else:
            self.fields['gender'].widget.attrs['class'] = 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'
        
        # Filter programs based on university
        if 'university' in self.data:
            try:
                university_id = int(self.data.get('university'))
                self.fields['program'].queryset = Program.objects.filter(university_id=university_id)
            except (ValueError, TypeError):
                pass
        elif self.initial.get('university'):
            self.fields['program'].queryset = Program.objects.filter(university_id=self.initial['university'])
            if from_program_page:
                self.fields['university'].widget.attrs['style'] = 'pointer-events: none; background-color: #f3f4f6;'
                self.fields['university'].widget.attrs['readonly'] = True
        else:
            self.fields['program'].queryset = Program.objects.none()

        # Handle Program and Level
        selected_program = None
        if 'program' in self.data:
            try:
                selected_program = Program.objects.get(pk=self.data.get('program'))
            except (ValueError, TypeError, Program.DoesNotExist):
                pass
        elif self.initial.get('program'):
            try:
                selected_program = Program.objects.get(pk=self.initial['program'])
                if from_program_page:
                    self.fields['program'].widget.attrs['style'] = 'pointer-events: none; background-color: #f3f4f6;'
                    self.fields['program'].widget.attrs['readonly'] = True
            except Program.DoesNotExist:
                pass
        
        if selected_program:
            self.fields['level'].initial = selected_program.type.level.name
            level_name = selected_program.type.level.name.lower()
            if 'bachelor' in level_name:
                self.fields['application_type'].initial = 'undergraduate'
            elif 'master' in level_name or 'phd' in level_name:
                self.fields['application_type'].initial = 'postgraduate'
            else:
                self.fields['application_type'].initial = 'diploma'

        if self.user:
            self.fields['phone'].initial = self.user.phone
            self.fields['gender'].initial = self.user.gender
            self.fields['nationality'].initial = self.user.nationality
            self.fields['date_of_birth'].initial = self.user.date_of_birth
            self.fields['passport_number'].initial = self.user.passport_number
            self.fields['passport_expiry'].initial = self.user.passport_expiry
            self.fields['address'].initial = self.user.address


class ApplicationStep2Form(forms.Form):
    """Step 2: Document Upload"""
    passport = forms.FileField(
        label="Passport Copy",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark',
            'accept': '.pdf,.jpg,.jpeg,.png'
        }),
        help_text="Upload a clear scan of your passport (optional)"
    )
    transcript = forms.FileField(
        label="Academic Transcript",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark',
            'accept': '.pdf,.jpg,.jpeg,.png'
        }),
        help_text="Upload your latest academic transcript (optional)"
    )
    other_documents = forms.FileField(
        label="Other Documents",
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark',
            'accept': '.pdf,.jpg,.jpeg,.png'
        }),
        help_text="Upload additional documents (certificates, recommendations, etc.)"
    )


class ApplicationStep3Form(forms.Form):
    """Step 3: English Proficiency (Conditional)"""
    
    # Option to use existing score or enter new
    use_existing_score = forms.BooleanField(
        required=False,
        initial=False,
        label="Use existing test score from my profile",
        widget=forms.CheckboxInput(attrs={
            'class': 'rounded border-[#e7e2da] dark:border-[#3a2d1b] text-primary focus:ring-primary',
            'onchange': 'toggleScoreFields(this)'
        })
    )
    
    existing_score = forms.ModelChoiceField(
        queryset=StudentTestScore.objects.none(),
        required=False,
        label="Select Test Score",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'
        })
    )
    
    # New score fields
    test_type = forms.ChoiceField(
        choices=StudentTestScore.TEST_TYPES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'
        })
    )
    test_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'
        })
    )
    listening_score = forms.DecimalField(
        required=False,
        max_digits=5,
        decimal_places=1,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
            'placeholder': 'e.g., 7.5'
        })
    )
    reading_score = forms.DecimalField(
        required=False,
        max_digits=5,
        decimal_places=1,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
            'placeholder': 'e.g., 7.5'
        })
    )
    speaking_score = forms.DecimalField(
        required=False,
        max_digits=5,
        decimal_places=1,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
            'placeholder': 'e.g., 7.5'
        })
    )
    writing_score = forms.DecimalField(
        required=False,
        max_digits=5,
        decimal_places=1,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
            'placeholder': 'e.g., 7.5'
        })
    )
    overall_score = forms.DecimalField(
        required=False,
        max_digits=5,
        decimal_places=1,
        widget=forms.NumberInput(attrs={
            'step': '0.1',
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
            'placeholder': 'e.g., 7.5'
        })
    )
    
    # Consent checkbox - REQUIRED
    consent_given = forms.BooleanField(
        required=True,
        label="I agree that TrikonED may store my details and share my profile with selected colleges and universities for the purpose of admissions, scholarships, and counselling.",
        widget=forms.CheckboxInput(attrs={
            'class': 'rounded border-border text-primary focus:ring-primary h-5 w-5'
        }),
        error_messages={
            'required': 'You must agree to the terms to submit your application.'
        }
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            # Get active test scores for this user
            from django.utils import timezone
            today = timezone.now().date()
            self.fields['existing_score'].queryset = StudentTestScore.objects.filter(
                student=user,
                expiry_date__gte=today
            )

