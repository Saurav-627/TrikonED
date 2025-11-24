# TrikonED - Complete Django Modular Project

## 🚀 Quick Start

### 1. Install UV and Dependencies

```bash
# Install UV package manager
pip install uv

# Run setup script
bash setup.sh
```

### 2. Activate Virtual Environment

```bash
source .venv/bin/activate
```

### 3. Create Database & Superuser

```bash
# Create migrations
uv run python manage.py makemigrations

# Apply migrations
uv run python manage.py migrate

# Create superuser (admin account)
uv run python manage.py createsuperuser
# Username: admin
# Email: admin@trikoned.ae
# Password: (your choice)
```

### 4. Build Tailwind CSS

```bash
npm run build
```

### 5. Run Development Server

```bash
# Option 1: Django dev server
uv run python manage.py runserver

# Option 2: Uvicorn (ASGI - recommended)
uv run uvicorn config.asgi:application --reload
```

Visit: http://localhost:8000

---

## 📁 Project Structure (Modular Apps)

```
TrikonED/
├── config/                    # Django project settings
│   ├── __init__.py
│   ├── settings.py           # Main settings
│   ├── urls.py               # Root URL config
│   ├── wsgi.py
│   └── asgi.py
│
├── core/                      # Core app (shared models, landing page)
│   ├── models.py             # Country, Emirate, Curriculum
│   ├── views.py              # Landing page view
│   ├── urls.py
│   ├── admin.py
│   └── apps.py
│
├── universities/              # Universities app
│   ├── models.py             # University, ContactInfo, EnrollmentStat, etc.
│   ├── views.py              # University list, detail views
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   └── apps.py
│
├── programs/                  # Programs app
│   ├── models.py             # Program, ProgramLevel, ProgramType, etc.
│   ├── views.py              # Program list, detail views
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   └── apps.py
│
├── students/                  # Students app (auth, profile, dashboard)
│   ├── models.py             # Student, StudentDocument
│   ├── views.py              # Auth views, dashboard, profile
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   └── apps.py
│
├── applications/              # Applications app
│   ├── models.py             # Application, ApplicationLog
│   ├── views.py              # Multi-step application views
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py
│   └── apps.py
│
├── templates/                 # Global templates
│   ├── base/
│   │   └── base.html
│   ├── components/
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   └── university_card.html
│   └── (app-specific templates in each app)
│
├── static/                    # Static files
│   ├── css/
│   │   ├── input.css
│   │   └── output.css (generated)
│   ├── js/
│   └── images/
│
├── media/                     # User uploads
│
├── manage.py                  # Django management script
├── setup.sh                   # Automated setup script
├── .env                       # Environment variables (create this)
├── requirements.txt           # Python dependencies
├── package.json               # Node dependencies
└── tailwind.config.js         # Tailwind configuration
```

---

## 🗄️ Database Models (Modular by App)

### Core App

- **Country** - Countries (UAE)
- **Emirate** - UAE Emirates
- **Curriculum** - Educational curricula

### Universities App

- **ContactInfo** - University contact details
- **University** - Main university model
- **EnrollmentStat** - Enrollment statistics
- **Scholarship** - Scholarships offered
- **VisaSponsorship** - Visa sponsorship details
- **UniversityCurriculum** - University-Curriculum junction

### Programs App

- **ProgramLevel** - Bachelor's, Master's, PhD
- **ProgramType** - Specific degree types
- **Program** - Programs offered by universities
- **AcademicIntake** - Enrollment periods
- **TuitionFee** - Program fees
- **EnglishRequirement** - Language requirements

### Students App

- **Student** - Student model (extends AbstractUser)
- **StudentDocument** - Documents uploaded by students
- **StudentUniversityVisit** - Visit tracking

### Applications App

- **Application** - Student applications
- **ApplicationLog** - Application status timeline

---

## 🎨 Design System

### Colors (Tailwind Config)

- Primary Gradient: `#FFF8E1` → `#FFF3B0`
- Accent Green: `#2DD4BF`
- Accent Orange: `#FB923C`
- Text Primary: `#0F172A`

### Typography

- Display: Poppins
- Body: Inter, Lato

---

## 🔧 Environment Variables

Create `.env` file in project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for development)
DATABASE_URL=sqlite:///db.sqlite3

# For PostgreSQL in production:
# DATABASE_URL=postgresql://user:password@localhost:5432/trikoned

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@trikoned.ae
```

---

## 📝 Key Commands (Using UV)

```bash
# Activate virtual environment
source .venv/bin/activate

# Run migrations
uv run python manage.py makemigrations
uv run python manage.py migrate

# Create superuser
uv run python manage.py createsuperuser

# Collect static files
uv run python manage.py collectstatic

# Run development server
uv run python manage.py runserver

# Run with Uvicorn (ASGI)
uv run uvicorn config.asgi:application --reload

# Create a new app (if needed)
uv run python manage.py startapp app_name
```

---

## 🎯 Features Implemented

### ✅ Modular Django Apps

- Core (shared models, landing)
- Universities (university management)
- Programs (program management)
- Students (auth, profile, dashboard)
- Applications (multi-step application flow)

### ✅ Complete ERD Implementation

- 20 models across 5 apps
- All relationships (ForeignKey, ManyToMany)
- Proper field types and validators

### ✅ Authentication & Authorization

- Custom Student model (extends AbstractUser)
- Email verification flow
- Protected routes

### ✅ Multi-Step Application Flow

- 4-step application process
- Session-based autosave
- Progress tracking

### ✅ Admin Panel

- Custom admin classes for all models
- Filters, search, ordering
- Inline editing

### ✅ Responsive UI

- Tailwind CSS
- Mobile-first design
- A-Z navigation
- Search and filters

---

## 🚀 Production Deployment

### 1. Update Settings

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
```

### 2. Use PostgreSQL

```env
DATABASE_URL=postgresql://user:password@localhost:5432/trikoned
```

### 3. Configure Email

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

### 4. Collect Static Files

```bash
uv run python manage.py collectstatic --noinput
```

### 5. Run with Gunicorn

```bash
uv run gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

---

## 📚 Admin Panel Access

After creating superuser, access admin panel at:
**http://localhost:8000/admin/**

### Default Superuser (you'll create this)

- Username: admin
- Email: admin@trikoned.ae
- Password: (your choice during createsuperuser)

### Admin Features

- Manage all 20 models
- Add universities, programs, students
- View applications and timeline
- Manage scholarships and curricula

---

## 🎓 Adding Sample Data

### Via Admin Panel

1. Login to admin: http://localhost:8000/admin/
2. Add data in this order:
   - Country (UAE)
   - Emirate (Dubai, Abu Dhabi, Sharjah)
   - ContactInfo
   - University
   - ProgramLevel (Bachelor's, Master's)
   - ProgramType (BSc Computer Science, etc.)
   - Program
   - Curriculum (IB, British, American)

### Via Django Shell

```bash
uv run python manage.py shell

from core.models import Country, Emirate
from universities.models import University

# Create UAE
uae = Country.objects.create(name="United Arab Emirates", iso_code="ARE")

# Create Emirates
dubai = Emirate.objects.create(name="Dubai", country=uae)
abudhabi = Emirate.objects.create(name="Abu Dhabi", country=uae)
```

---

## 🔍 Troubleshooting

### Issue: "No module named 'uv'"

**Solution**: Install UV first: `pip install uv`

### Issue: "Table doesn't exist"

**Solution**: Run migrations:

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

### Issue: "Tailwind CSS not loading"

**Solution**: Build Tailwind: `npm run build`

### Issue: "CSRF verification failed"

**Solution**: Ensure `{% csrf_token %}` is in all forms

---

## 📞 Support

For issues or questions:

1. Check this README
2. Review Django documentation: https://docs.djangoproject.com/
3. Check Tailwind documentation: https://tailwindcss.com/docs

---

## 🎉 You're Ready!

The project is fully set up with modular Django apps. Just run:

```bash
bash setup.sh
source .venv/bin/activate
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

**Happy Building! 🚀**
