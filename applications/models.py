"""
Applications App Models
"""
import uuid
from django.db import models


class Application(models.Model):
    """Student applications to universities"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='applications')
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='applications')
    program = models.ForeignKey('programs.Program', on_delete=models.CASCADE, related_name='applications')
    application_type = models.CharField(max_length=50, choices=[
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('diploma', 'Diploma'),
    ])
    status = models.CharField(max_length=50, choices=[
        ('draft', 'Draft'),
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='draft')
    applied_on = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True)
    consent_given = models.BooleanField(default=False)
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    application_id = models.CharField(max_length=20, unique=True, editable=False, null=True)
    lead_quality = models.CharField(
        max_length=20,
        choices=[
            ('high', 'High Lead'),
            ('medium', 'Medium Lead'),
            ('low', 'Low Lead'),
        ],
        default='low',
        help_text="Quality of the lead based on application completeness"
    )
    custom_status_message = models.TextField(
        blank=True,
        null=True,
        help_text="Custom message from admin (e.g., rejection reason, additional notes). If empty, default status message will be shown."
    )
    
    class Meta:
        ordering = ['-applied_on']
    
    def save(self, *args, **kwargs):
        if not self.application_id:
            last_app = Application.objects.filter(application_id__isnull=False).order_by('-application_id').first()
            if last_app and last_app.application_id.isdigit():
                self.application_id = f"{int(last_app.application_id) + 1:06d}"
            else:
                self.application_id = '000001'
        super().save(*args, **kwargs)
    
    def get_status_message(self):
        """Return custom status message if set, otherwise return default message based on status"""
        if self.custom_status_message:
            return self.custom_status_message
        
        # Default messages based on status
        default_messages = {
            'draft': 'Your application is saved as draft. Please complete and submit it.',
            'pending': 'Your application has been submitted and is pending review.',
            'under_review': 'Your application is currently under review by the admissions team.',
            'accepted': 'Congratulations! Your application has been accepted.',
            'rejected': 'Unfortunately, your application was not successful at this time.',
        }
        return default_messages.get(self.status, 'Application status updated.')
    
    def __str__(self):
        return f"#{self.application_id} - {self.student.username} → {self.university.short_name} ({self.status})"


class ApplicationLog(models.Model):
    """Application status timeline"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.application.id} - {self.event}"


class PendingApplication(Application):
    class Meta:
        proxy = True
        verbose_name = "Pending Application"
        verbose_name_plural = "Pending Applications"


class AcceptedApplication(Application):
    class Meta:
        proxy = True
        verbose_name = "Accepted Application"
        verbose_name_plural = "Accepted Applications"


class RejectedApplication(Application):
    class Meta:
        proxy = True
        verbose_name = "Rejected Application"
        verbose_name_plural = "Rejected Applications"
