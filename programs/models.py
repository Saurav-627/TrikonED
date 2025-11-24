"""
Programs App Models
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class ProgramLevel(models.Model):
    """Program levels: Bachelor's, Master's, PhD"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ProgramType(models.Model):
    """Specific degree types within a level"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    level = models.ForeignKey(ProgramLevel, on_delete=models.CASCADE, related_name='program_types')
    description = models.TextField(blank=True)
    duration = models.IntegerField()
    duration_unit = models.CharField(max_length=20, choices=[
        ('years', 'Years'),
        ('months', 'Months'),
        ('semesters', 'Semesters'),
    ], default='years')
    total_credits = models.IntegerField(null=True, blank=True)
    entry_requirements = models.TextField()
    
    class Meta:
        ordering = ['level', 'name']
        unique_together = [['name', 'level']]
    
    def __str__(self):
        return f"{self.name} ({self.level.name})"


class Program(models.Model):
    """Programs offered by universities"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey('universities.University', on_delete=models.CASCADE, related_name='programs')
    type = models.ForeignKey(ProgramType, on_delete=models.PROTECT, related_name='programs')
    name = models.CharField(max_length=255)
    description = models.TextField()
    delivery_type = models.CharField(max_length=50, choices=[
        ('on_campus', 'On Campus'),
        ('online', 'Online'),
        ('hybrid', 'Hybrid'),
    ], default='on_campus')
    department = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['university', 'name']
        unique_together = [['university', 'name']]
    
    def __str__(self):
        return f"{self.name} - {self.university.short_name}"


class AcademicIntake(models.Model):
    """Enrollment periods"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='intakes')
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    application_deadline = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-start_date']
    
    def __str__(self):
        return f"{self.name} - {self.program.name}"


class TuitionFee(models.Model):
    """Tuition fees for program types"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program_type = models.ForeignKey(ProgramType, on_delete=models.CASCADE, related_name='tuition_fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='AED')
    per = models.CharField(max_length=50, choices=[
        ('year', 'Per Year'),
        ('semester', 'Per Semester'),
        ('credit', 'Per Credit Hour'),
        ('program', 'Total Program'),
    ], default='year')
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['program_type', 'amount']
    
    def __str__(self):
        return f"{self.amount} {self.currency} {self.per}"


class EnglishRequirement(models.Model):
    """English language requirements"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='english_requirements')
    ielts = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(9)])
    toefl = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(120)])
    pte = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(90)])
    expiry_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.program.name} - English Requirements"
