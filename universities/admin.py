from django.contrib import admin
from .models import (
    ContactInfo, University, EnrollmentStat, Scholarship,
    VisaSponsorship, UniversityCurriculum
)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'website']
    search_fields = ['email', 'phone']


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_name', 'get_location', 'university_type', 'is_partner', 'ranking']
    list_filter = ['is_partner', 'university_type', 'location_emirate']
    search_fields = ['name', 'short_name', 'location_city']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'short_name', 'slug', 'image', 'logo')
        }),
        ('Location', {
            'fields': ('location_emirate', 'location_city'),
            'description': 'For UAE universities: Select emirate. For other countries: Enter city/state in "Location City" field.'
        }),
        ('Details', {
            'fields': ('description', 'established_year', 'university_type', 'is_partner', 'ranking')
        }),
        ('Additional Information', {
            'fields': ('accreditation', 'facilities', 'contact_info')
        }),
    )
    readonly_fields = ['id']
    actions = ['delete_all_universities']

    def get_location(self, obj):
        """Display location in admin list"""
        return obj.get_location_display()
    get_location.short_description = 'Location'
    get_location.admin_order_field = 'location_emirate'

    def delete_all_universities(self, request, queryset):
        # Delete all universities, not just the selected ones (if that's what "All data" means)
        # But usually actions apply to queryset. The user said "All data should get an option to delete".
        # If they select all, they can delete. But maybe they want a button to wipe everything?
        # I'll assume standard bulk delete is not enough? 
        # "All data should get an option to delete for admin" -> Maybe a button in the change list?
        # I'll stick to a custom action that deletes the selected ones, but maybe the user wants to delete EVERYTHING.
        # "All data" might refer to the whole DB? That's dangerous.
        # I'll implement an action that deletes all objects in the queryset.
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f"{count} universities deleted.")
    delete_all_universities.short_description = "Delete selected universities"


@admin.register(EnrollmentStat)
class EnrollmentStatAdmin(admin.ModelAdmin):
    list_display = ['get_university_name', 'academic_year', 'total_enrollment', 'faculty_count']
    list_filter = ['academic_year', 'university']
    search_fields = ['university__name', 'academic_year']
    autocomplete_fields = ['university']
    
    def get_university_name(self, obj):
        """Display full university name"""
        return obj.university.name
    get_university_name.short_description = 'University'
    get_university_name.admin_order_field = 'university__name'


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_university_name', 'amount', 'renewable']
    list_filter = ['renewable', 'university']
    search_fields = ['name', 'university__name', 'description']
    autocomplete_fields = ['university']
    
    def get_university_name(self, obj):
        """Display full university name"""
        return obj.university.name
    get_university_name.short_description = 'University'
    get_university_name.admin_order_field = 'university__name'


@admin.register(VisaSponsorship)
class VisaSponsorshipAdmin(admin.ModelAdmin):
    list_display = ['get_university_name', 'offers_visa']
    list_filter = ['offers_visa', 'university']
    search_fields = ['university__name']
    autocomplete_fields = ['university']
    
    def get_university_name(self, obj):
        """Display full university name"""
        return obj.university.name
    get_university_name.short_description = 'University'
    get_university_name.admin_order_field = 'university__name'


@admin.register(UniversityCurriculum)
class UniversityCurriculumAdmin(admin.ModelAdmin):
    list_display = ['get_university_name', 'curriculum']
    list_filter = ['university', 'curriculum']
    search_fields = ['university__name', 'curriculum__name']
    autocomplete_fields = ['university']
    
    def get_university_name(self, obj):
        """Display full university name"""
        return obj.university.name
    get_university_name.short_description = 'University'
    get_university_name.admin_order_field = 'university__name'
