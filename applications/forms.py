from django import forms
from .models import Application
from students.models import Student

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
        
        # Make personal info read-only
        personal_fields = ['phone', 'gender', 'nationality', 'date_of_birth', 'passport_number', 'passport_expiry', 'address']
        for field in personal_fields:
            self.fields[field].widget.attrs['readonly'] = True
            self.fields[field].widget.attrs['class'] = 'bg-gray-100 cursor-not-allowed'
        
        # Filter programs based on university
        if 'university' in self.data:
            try:
                university_id = int(self.data.get('university'))
                self.fields['program'].queryset = Program.objects.filter(university_id=university_id)
            except (ValueError, TypeError):
                pass
        elif self.initial.get('university'):
            self.fields['program'].queryset = Program.objects.filter(university_id=self.initial['university'])
            # If university is pre-filled from URL, disable the field
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
                # If program is pre-filled, disable the field
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
            student = self.user
            student.phone = self.cleaned_data['phone']
            student.gender = self.cleaned_data['gender']
            student.nationality = self.cleaned_data['nationality']
            student.date_of_birth = self.cleaned_data['date_of_birth']
            student.passport_number = self.cleaned_data['passport_number']
            student.passport_expiry = self.cleaned_data['passport_expiry']
            student.address = self.cleaned_data['address']
            student.save()
            
            application.student = student
        
        if commit:
            application.save()
        return application
