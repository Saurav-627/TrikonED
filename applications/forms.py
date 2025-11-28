from django import forms
from .models import Application
from students.models import Student

class ApplicationForm(forms.ModelForm):
    # Student fields
    phone = forms.CharField(required=True, label="Phone Number")
    gender = forms.ChoiceField(choices=Student._meta.get_field('gender').choices, required=True)
    nationality = forms.CharField(required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    passport_number = forms.CharField(required=True)
    passport_expiry = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)

    class Meta:
        model = Application
        fields = ['university', 'program', 'application_type', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
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
