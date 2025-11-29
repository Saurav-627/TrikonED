"""
Core Models - Shared models used across the application
"""
import uuid
from django.db import models


class Country(models.Model):
    """Country model - represents countries (primarily UAE)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    country_code = models.CharField(max_length=3, unique=True, help_text="ISO 3166-1 alpha-3 code")
    
    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']
        indexes = [models.Index(fields=['country_code'])]
    
    def __str__(self):
        return self.name


class Emirate(models.Model):
    """Emirate model - represents UAE emirates"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='emirates')
    
    class Meta:
        ordering = ['name']
        unique_together = [['name', 'country']]
        indexes = [models.Index(fields=['country', 'name'])]
    
    def __str__(self):
        return f"{self.name}, {self.country.name}"


class Curriculum(models.Model):
    """Curriculum model - educational curricula (IB, British, American, etc.)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    country_origin = models.CharField(max_length=100, help_text="Country where this curriculum originated")
    
    class Meta:
        verbose_name_plural = "Curricula"
        ordering = ['name']
    
    def __str__(self):
        return self.name
