from django.contrib import admin
from django import forms
from universities.models import University
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

class UniversityChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name  # Show full name instead of __str__

class AcademicIntakeForm(forms.ModelForm):
    university = UniversityChoiceField(
        queryset=University.objects.all(),
        required=False,
        label="University",
        help_text="Select university first to filter programs"
    )
    
    class Meta:
        model = AcademicIntake
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing existing object, set university from program
        if self.instance and self.instance.pk:
            try:
                if self.instance.program:
                    self.fields['university'].initial = self.instance.program.university
            except AcademicIntake.program.RelatedObjectDoesNotExist:
                pass
        
        # Filter programs based on university if provided
        if 'university' in self.data:
            try:
                university_id = int(self.data.get('university'))
                self.fields['program'].queryset = Program.objects.filter(university_id=university_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            try:
                if self.instance.program:
                    # When editing, show all programs from the same university
                    self.fields['program'].queryset = Program.objects.filter(
                        university=self.instance.program.university
                    ).order_by('name')
            except AcademicIntake.program.RelatedObjectDoesNotExist:
                pass

@admin.register(AcademicIntake)
class AcademicIntakeAdmin(admin.ModelAdmin):
    form = AcademicIntakeForm
    list_display = ['name', 'program', 'get_university', 'start_date', 'application_deadline']
    list_filter = ['start_date', 'program__university']
    search_fields = ['name', 'program__name', 'program__university__name']
    
    fieldsets = (
        (None, {
            'fields': ('university', 'name', 'program', 'start_date', 'end_date', 'application_deadline')
        }),
    )
    
    class Media:
        js = (
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/jquery.init.js',
            'programs/admin/js/filter_programs.js',
        )

    def get_university(self, obj):
        return obj.program.university.name
    get_university.short_description = 'University'
    get_university.admin_order_field = 'program__university__name'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Customize how foreign keys are displayed"""
        if db_field.name == "program":
            # Show full university name in program dropdown
            kwargs["queryset"] = Program.objects.select_related('university').all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('filter-programs/', self.admin_site.admin_view(self.filter_programs_view), name='academicintake_filter_programs'),
        ]
        return custom_urls + urls
    
    def filter_programs_view(self, request):
        from django.http import JsonResponse
        university_id = request.GET.get('university_id')
        if university_id:
            programs = Program.objects.filter(university_id=university_id).values('id', 'name').order_by('name')
            return JsonResponse(list(programs), safe=False)
        return JsonResponse([], safe=False)

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
