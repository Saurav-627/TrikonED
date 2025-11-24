import os
import django
import random
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Country, Emirate, Curriculum
from universities.models import University, ContactInfo
from programs.models import Program, ProgramLevel, ProgramType, TuitionFee, AcademicIntake

def populate():
    print("Creating Core Data...")
    
    # Countries
    uae, _ = Country.objects.get_or_create(name="United Arab Emirates", iso_code="ARE")
    
    # Emirates
    emirates_data = ["Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Ras Al Khaimah"]
    emirates = {}
    for name in emirates_data:
        emirate, _ = Emirate.objects.get_or_create(name=name, country=uae)
        emirates[name] = emirate
        print(f" - Created Emirate: {name}")

    # Curricula
    curricula_data = ["British Curriculum", "American Curriculum", "International Baccalaureate (IB)", "Indian (CBSE)"]
    for name in curricula_data:
        Curriculum.objects.get_or_create(name=name)
        print(f" - Created Curriculum: {name}")

    print("\nCreating Universities...")
    
    # University 1: Partner
    contact1 = ContactInfo.objects.create(
        email="admissions@trikon.edu.ae",
        phone="+971 4 123 4567",
        website="https://trikon.edu.ae",
        address="Knowledge Park, Dubai"
    )
    
    uni1, created = University.objects.get_or_create(
        name="Trikon University Dubai",
        defaults={
            'short_name': "TUD",
            'location_emirate': emirates["Dubai"],
            'contact_info': contact1,
            'is_partner': True,
            'description': "A premier institution focused on technology and innovation. Trikon University offers state-of-the-art facilities and a world-class curriculum designed to prepare students for the future.",
            'established_year': 2010,
            'accreditation': "MOE Accredited, KHDA Approved",
            'facilities': "Robotics Lab, AI Center, Library, Sports Complex",
            'ranking': 5,
            'university_type': 'private'
        }
    )
    if created: print(f" - Created Partner University: {uni1.name}")

    # University 2: Non-Partner
    contact2 = ContactInfo.objects.create(
        email="info@futurecollege.ae",
        phone="+971 2 987 6543",
        website="https://futurecollege.ae",
        address="Corniche Road, Abu Dhabi"
    )
    
    uni2, created = University.objects.get_or_create(
        name="UAE Future College",
        defaults={
            'short_name': "UFC",
            'location_emirate': emirates["Abu Dhabi"],
            'contact_info': contact2,
            'is_partner': False,
            'description': "Dedicated to fostering leadership and excellence in business and arts. Located in the heart of the capital.",
            'established_year': 1995,
            'accreditation': "MOE Accredited",
            'facilities': "Business Incubator, Art Studio, Auditorium",
            'ranking': 12,
            'university_type': 'public'
        }
    )
    if created: print(f" - Created University: {uni2.name}")

    # University 3: Partner
    contact3 = ContactInfo.objects.create(
        email="contact@globaltech.ae",
        phone="+971 6 555 1234",
        website="https://globaltech.ae",
        address="University City, Sharjah"
    )
    
    uni3, created = University.objects.get_or_create(
        name="Global Tech Institute",
        defaults={
            'short_name': "GTI",
            'location_emirate': emirates["Sharjah"],
            'contact_info': contact3,
            'is_partner': True,
            'description': "A hub for engineering and scientific research. Partnered with top global universities.",
            'established_year': 2015,
            'accreditation': "ABET Accredited",
            'facilities': "Engineering Labs, Research Center, Student Housing",
            'ranking': 8,
            'university_type': 'private'
        }
    )
    if created: print(f" - Created Partner University: {uni3.name}")

    print("\nCreating Programs...")
    
    # Program Levels
    bachelors, _ = ProgramLevel.objects.get_or_create(name="Bachelor's")
    masters, _ = ProgramLevel.objects.get_or_create(name="Master's")
    
    # Program Types
    cs_type, _ = ProgramType.objects.get_or_create(
        name="Computer Science",
        level=bachelors,
        defaults={'duration': 4, 'duration_unit': 'years', 'total_credits': 120, 'entry_requirements': "High School Diploma with 80%"}
    )
    
    mba_type, _ = ProgramType.objects.get_or_create(
        name="MBA",
        level=masters,
        defaults={'duration': 2, 'duration_unit': 'years', 'total_credits': 36, 'entry_requirements': "Bachelor's Degree + 2 years experience"}
    )

    # Programs
    p1, created = Program.objects.get_or_create(
        name="BSc in Artificial Intelligence",
        university=uni1,
        type=cs_type,
        defaults={
            'description': "Learn the fundamentals of AI and Machine Learning.",
            'delivery_type': 'on_campus',
            'department': "Computer Science"
        }
    )
    if created: print(f" - Created Program: {p1.name}")

    p2, created = Program.objects.get_or_create(
        name="Global MBA",
        university=uni2,
        type=mba_type,
        defaults={
            'description': "A comprehensive business program for future leaders.",
            'delivery_type': 'hybrid',
            'department': "Business School"
        }
    )
    if created: print(f" - Created Program: {p2.name}")
    
    p3, created = Program.objects.get_or_create(
        name="BSc in Cyber Security",
        university=uni3,
        type=cs_type,
        defaults={
            'description': "Protect the digital world with advanced security skills.",
            'delivery_type': 'on_campus',
            'department': "Engineering"
        }
    )
    if created: print(f" - Created Program: {p3.name}")

    print("\n✅ Data population complete!")

if __name__ == '__main__':
    populate()
