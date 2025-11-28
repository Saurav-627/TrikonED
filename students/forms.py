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
