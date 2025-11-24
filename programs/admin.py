from django.contrib import admin
from .models import ProgramLevel, ProgramType, Program, AcademicIntake, TuitionFee, EnglishRequirement

@admin.register(ProgramLevel)
class ProgramLevelAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ProgramType)
class ProgramTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'duration', 'duration_unit']
    list_filter = ['level']

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'type', 'delivery_type', 'is_active']
    list_filter = ['delivery_type', 'is_active', 'university']
    search_fields = ['name']

@admin.register(AcademicIntake)
class AcademicIntakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'program', 'start_date', 'application_deadline']

@admin.register(TuitionFee)
class TuitionFeeAdmin(admin.ModelAdmin):
    list_display = ['program_type', 'amount', 'currency', 'per']

@admin.register(EnglishRequirement)
class EnglishRequirementAdmin(admin.ModelAdmin):
    list_display = ['program', 'ielts', 'toefl', 'pte']
