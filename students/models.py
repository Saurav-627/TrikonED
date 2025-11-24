"""
Students App Models
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Student(AbstractUser):
    """Custom student model extending AbstractUser"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=20, choices=[
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    passport_number = models.CharField(max_length=50, blank=True)
    passport_expiry = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='student_profiles/', blank=True, null=True)
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name else self.username


class StudentDocument(models.Model):
    """Documents uploaded by students"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=100, choices=[
        ('passport', 'Passport'),
        ('transcript', 'Academic Transcript'),
        ('certificate', 'Certificate'),
        ('recommendation', 'Letter of Recommendation'),
        ('other', 'Other'),
    ])
    file_url = models.FileField(upload_to='documents/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.doc_type}"


class StudentUniversityVisit(models.Model):
    """Track student visits to university pages"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='university_visits')
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='student_visits')
    visited_at = models.DateTimeField(auto_now_add=True)
    visit_count = models.IntegerField(default=1)
    
    class Meta:
        unique_together = [['student', 'university']]
        ordering = ['-visited_at']
    
    def __str__(self):
        return f"{self.student.username} visited {self.university.short_name}"
