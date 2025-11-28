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
