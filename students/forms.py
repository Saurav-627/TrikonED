from django import forms
from .models import Student, StudentDocument, StudentTestScore

class StudentRegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
            'placeholder': 'Create a strong password'
        })
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
            'placeholder': 'Confirm your password'
        }),
        label="Confirm Password"
    )
    
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
                'placeholder': 'your.email@example.com'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        
        # Auto-generate username
        import random
        import string
        
        first_name = self.cleaned_data.get('first_name', '').lower()
        last_name = self.cleaned_data.get('last_name', '').lower()
        
        # Sanitize names to keep only alphanumeric characters
        first_name = "".join(c for c in first_name if c.isalnum())
        last_name = "".join(c for c in last_name if c.isalnum())
        
        base_username = f"{first_name}.{last_name}"
        username = base_username
        
        # Ensure uniqueness
        while Student.objects.filter(username=username).exists():
            random_suffix = ''.join(random.choices(string.digits, k=4))
            username = f"{base_username}{random_suffix}"
            
        user.username = username
        
        if commit:
            user.save()
        return user

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'phone', 'gender', 'nationality', 
                  'date_of_birth', 'passport_number', 'passport_expiry', 'address', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'}),
            'gender': forms.Select(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'}),
            'nationality': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'}),
            'passport_number': forms.TextInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'}),
            'passport_expiry': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'}),
            'profile_picture': forms.FileInput(attrs={'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'}),
        }

class MultipleDocumentUploadForm(forms.Form):
    passport = forms.FileField(
        label="Passport Copy",
        required=False,
        widget=forms.FileInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-accent-green'}),
        help_text="Upload a clear scan of your passport. Leave empty to keep existing."
    )
    transcript = forms.FileField(
        label="Academic Transcript",
        required=False,
        widget=forms.FileInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-accent-green'}),
        help_text="Upload your latest academic transcript or marksheet. Leave empty to keep existing."
    )
    other_documents = forms.FileField(
        label="Other Documents (Optional)",
        required=False,
        widget=forms.FileInput(attrs={'class': 'w-full px-4 py-3 border rounded-xl focus:ring-2 focus:ring-accent-green'}),
        help_text="You can select multiple files (e.g., Certificates, Recommendations)."
    )


class StudentTestScoreForm(forms.ModelForm):
    """Form for students to add their English proficiency test scores"""
    
    class Meta:
        model = StudentTestScore
        fields = ['test_type', 'test_date', 'listening_score', 'reading_score', 
                  'speaking_score', 'writing_score', 'overall_score', 'report_file']
        widgets = {
            'test_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark text-text-primary dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'
            }),
            'test_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 rounded-lg border border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark text-text-primary dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all'
            }),
            'listening_score': forms.NumberInput(attrs={
                'step': '0.1',
                'class': 'w-full px-4 py-3 rounded-lg border border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark text-text-primary dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
                'placeholder': 'e.g., 7.5'
            }),
            'reading_score': forms.NumberInput(attrs={
                'step': '0.1',
                'class': 'w-full px-4 py-3 rounded-lg border border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark text-text-primary dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
                'placeholder': 'e.g., 7.5'
            }),
            'speaking_score': forms.NumberInput(attrs={
                'step': '0.1',
                'class': 'w-full px-4 py-3 rounded-lg border border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark text-text-primary dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
                'placeholder': 'e.g., 7.5'
            }),
            'writing_score': forms.NumberInput(attrs={
                'step': '0.1',
                'class': 'w-full px-4 py-3 rounded-lg border border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark text-text-primary dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
                'placeholder': 'e.g., 7.5'
            }),
            'overall_score': forms.NumberInput(attrs={
                'step': '0.1',
                'class': 'w-full px-4 py-3 rounded-lg border border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark text-text-primary dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
                'placeholder': 'e.g., 7.5'
            }),
            'report_file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-border-light dark:border-border-dark bg-background-light dark:bg-background-dark text-text-primary dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all score fields optional
        for field in ['listening_score', 'reading_score', 'speaking_score', 'writing_score', 'overall_score', 'report_file']:
            self.fields[field].required = False

