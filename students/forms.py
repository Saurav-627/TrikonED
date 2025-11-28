from django import forms
from .models import Student, StudentDocument

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
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-[#e7e2da] dark:border-[#3a2d1b] bg-background-light dark:bg-background-dark text-[#181510] dark:text-white focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-all',
                'placeholder': 'Choose a username'
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
