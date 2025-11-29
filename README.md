# TrikonED - UAE University Discovery & Application Platform

A comprehensive Django-based platform for students to discover UAE universities, explore programs, and manage their applications with an intuitive interface and powerful features.

---

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
│   ├── views.py              # Landing, About, Contact pages
│   ├── backends.py           # Custom authentication backend
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       ├── core/
│       │   ├── landing.html
│       │   ├── about.html
│       │   └── contact.html
│       └── components/
│           ├── navbar.html
│           └── footer.html
│
├── universities/              # Universities app
│   ├── models.py             # University, ContactInfo, EnrollmentStat, Scholarship, VisaSponsorship
│   ├── views.py              # University list, detail views
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── universities/
│           ├── university_list.html
│           └── university_detail.html
│
├── programs/                  # Programs app
│   ├── models.py             # Program, ProgramLevel, ProgramType, TuitionFee, EnglishRequirement
│   ├── views.py              # Program list, detail views
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── programs/
│           ├── program_list.html
│           └── program_detail.html
│
├── students/                  # Students app (auth, profile, dashboard)
│   ├── models.py             # Student (custom user), StudentDocument, StudentUniversityVisit
│   ├── views.py              # Auth views, dashboard, profile, document upload
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py              # Registration, profile, document forms
│   └── templates/
│       └── students/
│           ├── login.html
│           ├── register.html
│           ├── dashboard.html
│           ├── profile.html
│           └── document_upload.html
│
├── applications/              # Applications app
│   ├── models.py             # Application, ApplicationLog, Proxy models
│   ├── views.py              # Application create, detail, PDF generation
│   ├── utils.py              # PDF generation utility
│   ├── urls.py
│   ├── admin.py
│   ├── forms.py              # Multi-step application form
│   └── templates/
│       └── applications/
│           ├── create.html
│           └── detail.html
│
├── templates/                 # Global templates
│   └── base/
│       └── base.html
│
├── static/                    # Static files
│   ├── css/
│   │   ├── input.css
│   │   └── output.css (generated)
│   ├── js/
│   └── images/
│
├── media/                     # User uploads
│   ├── university_images/
│   ├── university_logos/
│   └── student_documents/
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
  - `name`, `country_code` (renamed from iso_code)
- **Emirate** - UAE Emirates
  - `name`, `country` (FK to Country)
- **Curriculum** - Educational curricula
  - `name`, `description`

### Universities App

- **ContactInfo** - University contact details
  - `email`, `phone`, `website`, `address`
- **University** - Main university model
  - `name`, `short_name`, `location_emirate`, `contact_info`, `is_partner`, `description`, `established_year`, `accreditation`, `facilities`, `ranking`, `university_type`, `slug`
- **EnrollmentStat** - Enrollment statistics
  - `university`, `total_enrollment`, `international_enrollment`, `male_students`, `female_students`, `faculty_count`, `extra_data` (JSONField), `academic_year`
- **Scholarship** - Scholarships offered
  - `university`, `name`, `amount`, `eligibility`, `coverage`, `renewable`, `application_deadline`
- **VisaSponsorship** - Visa sponsorship details
  - `university`, `offers_visa`, `details`
- **UniversityCurriculum** - University-Curriculum junction
  - `university`, `curriculum`

### Programs App

- **ProgramLevel** - Bachelor's, Master's, PhD
  - `name`, `description`
- **ProgramType** - Specific degree types
  - `name`, `level`, `description`, `duration`, `duration_unit`, `total_credits`, `entry_requirements`
- **Program** - Programs offered by universities
  - `university`, `type`, `name`, `description`, `delivery_type`, `department`, `is_active`, `slug`
- **AcademicIntake** - Enrollment periods
  - `program`, `name`, `start_date`, `end_date`, `application_deadline`
- **TuitionFee** - Program fees
  - `program`, `amount`, `max_amount`, `currency`, `per`, `notes`
- **EnglishRequirement** - Language requirements
  - `program`, `ielts`, `toefl`, `pte`, `extra_requirements` (JSONField), `expiry_date`

### Students App

- **Student** - Student model (extends AbstractUser)
  - All Django User fields plus: `phone`, `gender`, `nationality`, `date_of_birth`, `passport_number`, `passport_expiry`, `address`, `profile_picture`
- **StudentDocument** - Documents uploaded by students
  - `student`, `doc_type`, `file_url`, `file_name`, `uploaded_at`
- **StudentUniversityVisit** - Visit tracking
  - `student`, `university`, `visit_count`, `last_visited`

### Applications App

- **Application** - Student applications
  - `application_id`, `student`, `university`, `program`, `status`, `applied_on`, `personal_info` (JSONField), `academic_info` (JSONField), `additional_info` (JSONField)
- **ApplicationLog** - Application status timeline
  - `application`, `status`, `notes`, `created_at`, `created_by`
- **Proxy Models** (for admin filtering)
  - `PendingApplication`, `AcceptedApplication`, `RejectedApplication`

---

## 🎨 Design System

### Theme Colors

**Primary Colors:**

- Primary Orange: `#ff9900` - Main brand color (buttons, links, accents)
- Highlight Yellow: `#FFC107` - Accent highlights

**Text Colors (Light Mode):**

- Text Dark: `#181510` - Primary text, headings
- Text Muted: `#8d7a5e` - Secondary text, descriptions

**Text Colors (Dark Mode):**

- Text Muted Dark: `#a19077` - Secondary text in dark mode

**Background Colors:**

- Background Light: `#f8f7f5` - Page background (light mode)
- Background Dark: `#231b0f` - Page background (dark mode)
- Card Dark: `#1a1307` - Card backgrounds (dark mode)

**Border Colors:**

- Border Light: `#e7e2da` - Borders (light mode)
- Border Dark: `#3a2d1b` - Borders (dark mode)

### Typography

- Display: Inter, Poppins
- Body: Inter, Lato, system-ui

### Design Features

- Warm, earthy color palette
- Fully responsive (mobile-first)
- Dark mode support throughout
- Smooth transitions and hover effects
- Material Symbols icons
- Tailwind CSS utility classes

---

## ✨ Key Features

### 🎯 For Students

1. **University Discovery**

   - Browse 100+ universities
   - Filter by emirate, type, partner status
   - A-Z navigation
   - Search functionality
   - Grid/List view toggle

2. **Program Exploration**

   - Detailed program information
   - Tuition fees, duration, intakes
   - English requirements (IELTS, TOEFL, PTE)
   - Curriculum details
   - Tab-based navigation

3. **Application Management**

   - Multi-step application form
   - Profile completion tracking
   - Document upload (passport, transcript)
   - Application status tracking
   - Timeline visualization
   - PDF generation for applications

4. **Student Dashboard**

   - Application overview
   - Profile completion indicator
   - Document management
   - Quick actions
   - Statistics cards

5. **Authentication**
   - Email or username login
   - Auto-generated usernames from first/last name
   - Profile management
   - Document upload and replacement

### 🔧 For Administrators

1. **Admin Panel Enhancements**

   - Proxy models for application filtering (Pending, Accepted, Rejected)
   - PDF download for applications
   - Bulk delete actions
   - Advanced search and filters
   - Autocomplete fields
   - Inline editing

2. **University Management**

   - Complete university profiles
   - Enrollment statistics with extra_data JSONField
   - Scholarship management
   - Visa sponsorship details
   - Accepted curricula

3. **Program Management**

   - Program types and levels
   - Tuition fee ranges
   - English requirements with extra_requirements JSONField
   - Academic intakes
   - Delivery types (on-campus, online, hybrid)

4. **Analytics**
   - Student visit tracking (university-level only)
   - Application statistics
   - Enrollment trends

### 🎨 UI/UX Features

1. **Responsive Design**

   - Mobile-first approach
   - Tablet and desktop optimized
   - Touch-friendly interactions

2. **Dark Mode**

   - Full dark mode support
   - Automatic theme detection
   - Manual toggle

3. **Interactive Elements**

   - Animated counters on landing page
   - Smooth scroll animations
   - Hover effects
   - Tab switching (client-side)
   - Progress indicators

4. **Accessibility**
   - WCAG AA compliant colors
   - Semantic HTML
   - Keyboard navigation
   - Screen reader friendly

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
uv run python manage.py collectstatic --noinput

# Run development server
uv run python manage.py runserver

# Run with Uvicorn (ASGI)
uv run uvicorn config.asgi:application --reload

# Build Tailwind CSS
npm run build

# Watch Tailwind CSS (development)
npm run dev
```

---

## 🚀 Production Deployment

### 1. Update Settings

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings (already in settings.py for production)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
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
EMAIL_HOST_PASSWORD=your-app-password
```

### 4. Collect Static Files

```bash
npm run build
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

### Admin Features

- Manage all 20+ models
- Add universities, programs, students
- View applications with status filtering
- Download application PDFs
- Manage scholarships and curricula
- Track enrollment statistics
- Bulk operations

---

## 🎓 Adding Sample Data

### Option 1: Via Admin Panel

1. Login to admin: http://localhost:8000/admin/
2. Add data in this order:
   - Country (UAE)
   - Emirate (Dubai, Abu Dhabi, Sharjah, Ajman, Ras Al Khaimah)
   - Curriculum (IB, British, American, Indian CBSE)
   - ContactInfo
   - University
   - ProgramLevel (Bachelor's, Master's, PhD)
   - ProgramType (BSc Computer Science, MBA, etc.)
   - Program
   - TuitionFee
   - EnglishRequirement
   - AcademicIntake
   - Scholarship
   - VisaSponsorship

### Option 2: Via Django Shell

```bash
uv run python manage.py shell

from core.models import Country, Emirate, Curriculum
from universities.models import University, ContactInfo

# Create UAE
uae = Country.objects.create(name="United Arab Emirates", country_code="ARE")

# Create Emirates
dubai = Emirate.objects.create(name="Dubai", country=uae)
abudhabi = Emirate.objects.create(name="Abu Dhabi", country=uae)
sharjah = Emirate.objects.create(name="Sharjah", country=uae)

# Create Curricula
ib = Curriculum.objects.create(name="International Baccalaureate (IB)")
british = Curriculum.objects.create(name="British Curriculum")
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

**Solution**: Build Tailwind:

```bash
npm install
npm run build
```

### Issue: "CSRF verification failed"

**Solution**: Ensure `{% csrf_token %}` is in all forms

### Issue: "Static files not found"

**Solution**: Collect static files:

```bash
uv run python manage.py collectstatic --noinput
```

### Issue: "Multiple authentication backends error"

**Solution**: This is already handled in the code. The custom `EmailOrUsernameModelBackend` is configured in settings.

---

## 🛠️ Recent Updates & Fixes

### Authentication & Registration

- ✅ Auto-generated usernames from first name + last name
- ✅ Email or username login support
- ✅ Custom authentication backend

### Application System

- ✅ PDF generation for applications
- ✅ Profile completion enforcement
- ✅ Read-only fields for completed profile data
- ✅ Application status proxy models for admin filtering

### Document Management

- ✅ Document upload with replacement functionality
- ✅ View existing documents before upload
- ✅ Support for passport, transcript, and other documents

### UI/UX Improvements

- ✅ Profile incomplete warning on dashboard
- ✅ Client-side tab switching (no page reloads)
- ✅ Visit count tracking (university-level only, not tab switches)
- ✅ Animated counters on landing page
- ✅ Dark mode throughout

### Admin Enhancements

- ✅ PDF download button for applications
- ✅ Proxy models for filtering by status
- ✅ Bulk delete actions for universities
- ✅ Autocomplete fields for better UX

---

## 📞 Support

For issues or questions:

1. Check this README
2. Review Django documentation: https://docs.djangoproject.com/
3. Check Tailwind documentation: https://tailwindcss.com/docs
4. Review Material Symbols: https://fonts.google.com/icons

---

## 🎉 You're Ready!

The project is fully set up with modular Django apps. Just run:

```bash
bash setup.sh
source .venv/bin/activate
uv run python manage.py migrate
uv run python manage.py createsuperuser
npm run build
uv run python manage.py runserver
```

Visit **http://localhost:8000** and start exploring!

**Happy Building! 🚀**

---

## 📄 License

This project is proprietary and confidential.

## 👥 Contributors

- Development Team: TrikonED

---

**Version**: 1.0.0  
**Last Updated**: November 2025
