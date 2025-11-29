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
    list_display = ['name', 'short_name', 'location_emirate', 'university_type', 'is_partner', 'ranking']
    list_filter = ['is_partner', 'university_type', 'location_emirate']
    search_fields = ['name', 'short_name']
    readonly_fields = ['id']
    actions = ['delete_all_universities']

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
    list_display = ['university', 'academic_year', 'total_enrollment', 'faculty_count']
    list_filter = ['academic_year']


@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'amount', 'renewable']
    list_filter = ['renewable', 'university']


@admin.register(VisaSponsorship)
class VisaSponsorshipAdmin(admin.ModelAdmin):
    list_display = ['university', 'offers_visa']
    list_filter = ['offers_visa']


@admin.register(UniversityCurriculum)
class UniversityCurriculumAdmin(admin.ModelAdmin):
    list_display = ['university', 'curriculum']
    list_filter = ['university']
