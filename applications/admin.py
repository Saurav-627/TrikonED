from django.contrib import admin
from .models import Application, ApplicationLog, PendingApplication, AcceptedApplication, RejectedApplication

class ApplicationLogInline(admin.TabularInline):
    model = ApplicationLog
    extra = 0
    readonly_fields = ['timestamp', 'event']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_id', 'student', 'university', 'program', 'status', 'lead_quality', 'applied_on', 'download_pdf_link']
    list_filter = ['status', 'lead_quality', 'application_type', 'applied_on']
    search_fields = ['application_id', 'student__username', 'student__email', 'university__name', 'program__name']
    inlines = [ApplicationLogInline]
    readonly_fields = ['application_id', 'applied_on', 'created_at', 'updated_at']
    actions = ['clear_custom_message', 'clear_remarks', 'clear_both_messages', 'reset_lead_quality']
    
    fieldsets = (
        ('Application Information', {
            'fields': ('application_id', 'student', 'university', 'program', 'application_type')
        }),
        ('Status & Quality', {
            'fields': ('status', 'lead_quality', 'custom_status_message'),
            'description': 'Set status and optionally add a custom message (e.g., rejection reason). If custom message is empty, a default message based on status will be shown to the student.'
        }),
        ('Additional Information', {
            'fields': ('remarks', 'consent_given', 'terms_accepted')
        }),
        ('Timestamps', {
            'fields': ('applied_on', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student', 'university', 'program')
    
    def download_pdf_link(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        url = reverse('applications:pdf', args=[obj.application_id])
        return format_html('<a href="{}" target="_blank" class="button">Download PDF</a>', url)
    download_pdf_link.short_description = 'PDF'
    
    # Custom Admin Actions
    def clear_custom_message(self, request, queryset):
        """Clear custom status message from selected applications"""
        updated = queryset.update(custom_status_message=None)
        self.message_user(request, f'{updated} application(s) had their custom status message cleared.')
    clear_custom_message.short_description = "Clear custom status message"
    
    def clear_remarks(self, request, queryset):
        """Clear remarks from selected applications"""
        updated = queryset.update(remarks='')
        self.message_user(request, f'{updated} application(s) had their remarks cleared.')
    clear_remarks.short_description = "Clear remarks"
    
    def clear_both_messages(self, request, queryset):
        """Clear both custom status message and remarks"""
        updated = queryset.update(custom_status_message=None, remarks='')
        self.message_user(request, f'{updated} application(s) had both custom message and remarks cleared.')
    clear_both_messages.short_description = "Clear custom message & remarks"
    
    def reset_lead_quality(self, request, queryset):
        """Reset lead quality to default (low)"""
        updated = queryset.update(lead_quality='low')
        self.message_user(request, f'{updated} application(s) had their lead quality reset to Low.')
    reset_lead_quality.short_description = "Reset lead quality to Low"
    
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
