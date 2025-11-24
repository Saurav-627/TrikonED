"""
Universities App Models
Complete implementation of university-related models
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import Emirate, Curriculum


class ContactInfo(models.Model):
    """Contact information for universities"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.TextField(blank=True)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=50)
    website = models.URLField(max_length=500, blank=True)
    
    class Meta:
        verbose_name_plural = "Contact Information"
    
    def __str__(self):
        return f"Contact: {self.email}"


class University(models.Model):
    """Main university model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='university_images/', blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=50, blank=True)
    location_emirate = models.ForeignKey(Emirate, on_delete=models.PROTECT, related_name='universities')
    contact_info = models.ForeignKey(ContactInfo, on_delete=models.CASCADE, related_name='universities')
    is_partner = models.BooleanField(default=False)
    description = models.TextField()
    established_year = models.IntegerField(validators=[MinValueValidator(1800), MaxValueValidator(2100)])
    accreditation = models.TextField()
    facilities = models.TextField()
    ranking = models.IntegerField(null=True, blank=True)
    university_type = models.CharField(max_length=50, choices=[
        ('public', 'Public'),
        ('private', 'Private'),
        ('federal', 'Federal'),
    ], default='private')
    
    class Meta:
        verbose_name_plural = "Universities"
        ordering = ['name']
        indexes = [
            models.Index(fields=['location_emirate', 'is_partner']),
            models.Index(fields=['university_type']),
        ]
    
    def __str__(self):
        return self.short_name or self.name


class EnrollmentStat(models.Model):
    """Enrollment statistics"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='enrollment_stats')
    total_enrollment = models.IntegerField(validators=[MinValueValidator(0)])
    international_enrollment = models.IntegerField(validators=[MinValueValidator(0)])
    male_students = models.IntegerField(validators=[MinValueValidator(0)])
    female_students = models.IntegerField(validators=[MinValueValidator(0)])
    faculty_count = models.IntegerField(validators=[MinValueValidator(0)])
    academic_year = models.CharField(max_length=20)
    
    class Meta:
        verbose_name_plural = "Enrollment Statistics"
        ordering = ['-academic_year']
        unique_together = [['university', 'academic_year']]
    
    def __str__(self):
        return f"{self.university.short_name} - {self.academic_year}"


class Scholarship(models.Model):
    """Scholarships offered by universities"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='scholarships')
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    eligibility = models.TextField()
    coverage = models.TextField()
    renewable = models.BooleanField(default=False)
    application_deadline = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['university', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.university.short_name}"


class VisaSponsorship(models.Model):
    """Visa sponsorship information"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='visa_sponsorships')
    offers_visa = models.BooleanField(default=True)
    details = models.TextField()
    
    class Meta:
        verbose_name_plural = "Visa Sponsorships"
    
    def __str__(self):
        return f"{self.university.short_name} - Visa Sponsorship"


class UniversityCurriculum(models.Model):
    """University-Curriculum junction table"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='accepted_curricula')
    curriculum = models.ForeignKey(Curriculum, on_delete=models.CASCADE, related_name='universities')
    
    class Meta:
        verbose_name_plural = "University Curricula"
        unique_together = [['university', 'curriculum']]
    
    def __str__(self):
        return f"{self.university.short_name} accepts {self.curriculum.name}"
