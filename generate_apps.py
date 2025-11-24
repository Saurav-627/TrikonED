#!/usr/bin/env python3
"""
TrikonED Project Generator
Generates all modular Django app files
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# App configurations
APPS = {
    'universities': {
        'models': ['ContactInfo', 'University', 'EnrollmentStat', 'Scholarship', 'VisaSponsorship', 'UniversityCurriculum'],
        'has_forms': True,
        'has_views': True,
    },
    'programs': {
        'models': ['ProgramLevel', 'ProgramType', 'Program', 'AcademicIntake', 'TuitionFee', 'EnglishRequirement'],
        'has_forms': True,
        'has_views': True,
    },
    'students': {
        'models': ['Student', 'StudentDocument', 'StudentUniversityVisit'],
        'has_forms': True,
        'has_views': True,
    },
    'applications': {
        'models': ['Application', 'ApplicationLog'],
        'has_forms': True,
        'has_views': True,
    },
}

def create_init_files():
    """Create __init__.py files for all apps"""
    for app_name in APPS.keys():
        init_file = BASE_DIR / app_name / '__init__.py'
        init_file.touch()
        
        migrations_init = BASE_DIR / app_name / 'migrations' / '__init__.py'
        migrations_init.touch()
    
    print("✅ Created __init__.py files")

def create_apps_py():
    """Create apps.py for each app"""
    for app_name in APPS.keys():
        class_name = ''.join(word.capitalize() for word in app_name.split('_'))
        content = f"""from django.apps import AppConfig


class {class_name}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = '{app_name}'
    verbose_name = '{class_name}'
"""
        apps_file = BASE_DIR / app_name / 'apps.py'
        apps_file.write_text(content)
    
    print("✅ Created apps.py files")

if __name__ == '__main__':
    print("🚀 Generating TrikonED modular app files...")
    create_init_files()
    create_apps_py()
    print("✅ All files generated successfully!")
