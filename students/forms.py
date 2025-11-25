from django import forms
from .models import Student, StudentDocument

class StudentRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-accent-green'}))
    
    class Meta:
        model = Student
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-accent-green'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-accent-green'}),
        }

class MultipleDocumentUploadForm(forms.Form):
    passport = forms.FileField(
        label="Passport Copy",
        widget=forms.FileInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-accent-green'}),
        help_text="Upload a clear scan of your passport."
    )
    transcript = forms.FileField(
        label="Academic Transcript",
        widget=forms.FileInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-accent-green'}),
        help_text="Upload your latest academic transcript or marksheet."
    )
    other_documents = forms.FileField(
        label="Other Documents (Optional)",
        required=False,
        widget=forms.FileInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-accent-green'}),
        help_text="You can select multiple files (e.g., Certificates, Recommendations)."
    )
