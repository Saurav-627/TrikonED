from django.contrib import admin
from .models import ProgramLevel, ProgramType, Program, AcademicIntake, TuitionFee, EnglishRequirement

@admin.register(ProgramLevel)
class ProgramLevelAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(ProgramType)
class ProgramTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'duration', 'duration_unit']
    list_filter = ['level']

class TuitionFeeInline(admin.TabularInline):
    model = TuitionFee
    extra = 1

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'type', 'delivery_type', 'is_active']
    list_filter = ['delivery_type', 'is_active', 'university']
    search_fields = ['name', 'university__name']
    inlines = [TuitionFeeInline]

@admin.register(AcademicIntake)
class AcademicIntakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'program', 'start_date', 'application_deadline']

@admin.register(TuitionFee)
class TuitionFeeAdmin(admin.ModelAdmin):
    list_display = ['program', 'get_university', 'amount', 'max_amount', 'currency', 'per']
    search_fields = ['program__name', 'program__university__name']
    list_filter = ['program__university']
    autocomplete_fields = ['program']

    def get_university(self, obj):
        return obj.program.university
    get_university.short_description = 'University'
    get_university.admin_order_field = 'program__university'

@admin.register(EnglishRequirement)
class EnglishRequirementAdmin(admin.ModelAdmin):
    list_display = ['program', 'ielts', 'toefl', 'pte']
    search_fields = ['program__name']
