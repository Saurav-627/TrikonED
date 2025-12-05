from django.contrib import admin
from .models import Application, ApplicationLog, PendingApplication, AcceptedApplication, RejectedApplication

class ApplicationLogInline(admin.TabularInline):
    model = ApplicationLog
    extra = 0
    readonly_fields = ['timestamp', 'event']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_id', 'student', 'university', 'program', 'status', 'applied_on', 'download_pdf_link']
    list_filter = ['status', 'application_type']
    search_fields = ['student__username', 'university__name', 'application_id']
    inlines = [ApplicationLogInline]
    readonly_fields = ['application_id', 'applied_on', 'created_at', 'updated_at']
    
    def download_pdf_link(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        url = reverse('applications:pdf', args=[obj.application_id])
        return format_html('<a href="{}" target="_blank" class="button">Download PDF</a>', url)
    download_pdf_link.short_description = 'PDF'
    
    def save_model(self, request, obj, form, change):
        # Track status changes
        if change and 'status' in form.changed_data:
            old_status = Application.objects.get(pk=obj.pk).status
            new_status = obj.status
            
            # Save the application first
            super().save_model(request, obj, form, change)
            
            # Create log entry for status change
            status_messages = {
                'pending': 'Application is pending review',
                'under_review': 'Application is now under review by the TrikonED team',
                'accepted': 'Congratulations! Your application has been accepted',
                'rejected': 'Unfortunately, your application was not successful at this time',
            }
            
            ApplicationLog.objects.create(
                application=obj,
                event=f'Status Changed: {old_status.title()} → {new_status.title()}',
                details=status_messages.get(new_status, f'Application status updated to {new_status}')
            )
        else:
            super().save_model(request, obj, form, change)

@admin.register(PendingApplication)
class PendingApplicationAdmin(ApplicationAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='pending')

@admin.register(AcceptedApplication)
class AcceptedApplicationAdmin(ApplicationAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='accepted')

@admin.register(RejectedApplication)
class RejectedApplicationAdmin(ApplicationAdmin):
    def get_queryset(self, request):
        return super().get_queryset(request).filter(status='rejected')

@admin.register(ApplicationLog)
class ApplicationLogAdmin(admin.ModelAdmin):
    list_display = ['application', 'event', 'timestamp']
    readonly_fields = ['timestamp']
