from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, StudentDocument, StudentUniversityVisit

@admin.register(Student)
class StudentAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'email_verified']
    list_filter = ['email_verified', 'gender']
    fieldsets = UserAdmin.fieldsets + (
        ('Personal Info', {'fields': ('phone', 'gender', 'nationality', 'date_of_birth', 'address')}),
        ('Passport', {'fields': ('passport_number', 'passport_expiry')}),
        ('Verification', {'fields': ('email_verified', 'verification_token')}),
    )

@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display = ['student', 'doc_type', 'file_name', 'uploaded_at']
    list_filter = ['doc_type']

@admin.register(StudentUniversityVisit)
class StudentUniversityVisitAdmin(admin.ModelAdmin):
    list_display = ['student', 'university', 'visited_at', 'visit_count']
