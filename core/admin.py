from django.contrib import admin
from .models import Country, Emirate, Curriculum


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'country_code')
    search_fields = ('name', 'country_code')


@admin.register(Emirate)
class EmirateAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    list_filter = ['country']
    search_fields = ['name']


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ['name', 'country_origin']
    search_fields = ['name', 'country_origin']
