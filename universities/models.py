"""
Universities App Models
Complete implementation of university-related models
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
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
    logo = models.ImageField(upload_to='university_logos/', blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=50, blank=True)
    location_emirate = models.ForeignKey(
        Emirate, 
        on_delete=models.PROTECT, 
        related_name='universities',
        null=True,
        blank=True,
        help_text="Select emirate if university is in UAE, otherwise leave blank"
    )
    country = models.ForeignKey(
        'core.Country',
        on_delete=models.PROTECT,
        related_name='universities',
        null=True,
        blank=True,
        help_text="Select country for non-UAE universities"
    )
    location_city = models.CharField(
        max_length=255,
        blank=True,
        help_text="City/State name for non-UAE universities (e.g., Sydney, Melbourne)"
    )
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
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Universities"
        ordering = ['name']
        indexes = [
            models.Index(fields=['location_emirate', 'is_partner']),
            models.Index(fields=['country']),
            models.Index(fields=['slug']),
        ]
    
    def get_location_display(self):
        """Return location string - emirate for UAE, city for others"""
        if self.location_emirate:
            return f"{self.location_emirate.name}, {self.location_emirate.country.name}"
        elif self.country and self.location_city:
            return f"{self.location_city}, {self.country.name}"
        elif self.location_city:
            return self.location_city
        elif self.country:
            return self.country.name
        return "Location not specified"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.short_name or self.name


class EnrollmentStat(models.Model):
    """Enrollment statistics"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='enrollment_stats')
    academic_year = models.CharField(max_length=20, blank=True, help_text="e.g., 2023-2024")
    total_enrollment = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="Total number of students"
    )
    international_enrollment = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="Number of international students"
    )
    male_students = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    female_students = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    faculty_count = models.IntegerField(
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text="Number of faculty members"
    )
    extra_data = models.JSONField(default=dict, blank=True, help_text="Additional statistics")
    
    class Meta:
        verbose_name_plural = "Enrollment Statistics"
    
    def __str__(self):
        return f"{self.university.name} - {self.academic_year if self.academic_year else 'No Year'}"


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
