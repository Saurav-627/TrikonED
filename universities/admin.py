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
