from django.contrib import admin
from .models import Application, ApplicationLog

class ApplicationLogInline(admin.TabularInline):
    model = ApplicationLog
    extra = 0
    readonly_fields = ['timestamp', 'event']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'university', 'program', 'status', 'applied_on']
    list_filter = ['status', 'application_type']
    search_fields = ['student__username', 'university__name']
    inlines = [ApplicationLogInline]

@admin.register(ApplicationLog)
class ApplicationLogAdmin(admin.ModelAdmin):
    list_display = ['application', 'event', 'timestamp']
    readonly_fields = ['timestamp']
