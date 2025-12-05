from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Student, StudentDocument, StudentUniversityVisit, StudentTestScore

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
    list_display = ['student', 'university', 'first_visit_date', 'latest_visit_date', 'visit_count']
    list_filter = ['university']
    search_fields = ['student__username', 'university__name']

@admin.register(StudentTestScore)
class StudentTestScoreAdmin(admin.ModelAdmin):
    list_display = ['student', 'test_type', 'overall_score', 'test_date', 'expiry_date', 'is_expired']
    list_filter = ['test_type', 'test_date']
    search_fields = ['student__username']
    readonly_fields = ['expiry_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Student & Test Info', {
            'fields': ('student', 'test_type', 'test_date', 'validity_years', 'expiry_date')
        }),
        ('Scores', {
            'fields': ('listening_score', 'reading_score', 'speaking_score', 'writing_score', 'overall_score')
        }),
        ('Report', {
            'fields': ('report_file',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_expired(self, obj):
        from django.utils import timezone
        if obj.expiry_date:
            return obj.expiry_date < timezone.now().date()
        return False
    is_expired.boolean = True
    is_expired.short_description = 'Expired'
