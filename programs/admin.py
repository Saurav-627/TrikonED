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
    list_display = ['name', 'get_university_name', 'type', 'delivery_type', 'is_active', 'slug']
    list_filter = ['type', 'delivery_type', 'is_active', 'university']
    search_fields = ['name', 'university__name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    autocomplete_fields = ['university']
    inlines = [TuitionFeeInline]
    
    def get_university_name(self, obj):
        """Display full university name instead of short name"""
        return obj.university.name
    get_university_name.short_description = 'University'
    get_university_name.admin_order_field = 'university__name'

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
    list_display = ['program', 'test_type', 'overall_score', 'listening_score', 'reading_score', 'speaking_score', 'writing_score']
    list_filter = ['test_type']
    search_fields = ['program__name']
    fieldsets = (
        ('Test Information', {
            'fields': ('program', 'test_type', 'custom_range_label')
        }),
        ('Scores', {
            'fields': ('listening_score', 'reading_score', 'speaking_score', 'writing_score', 'overall_score')
        }),
        ('Additional Requirements', {
            'fields': ('extra_requirements',)
        }),
    )
