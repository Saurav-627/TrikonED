#!/bin/bash
# Complete TrikonED Setup - One Command Setup

echo "🚀 TrikonED - Complete Modular Django Project Setup"
echo "===================================================="
echo ""

# Step 1: Install UV
echo "📦 Step 1/7: Installing UV package manager..."
pip install uv
echo "✅ UV installed"
echo ""

# Step 2: Create virtual environment
echo "🔧 Step 2/7: Creating virtual environment..."
uv venv
echo "✅ Virtual environment created"
echo ""

# Step 3: Install Python dependencies
echo "📥 Step 3/7: Installing Python dependencies with UV..."
source .venv/bin/activate
uv pip install Django==4.2.8
uv pip install django-environ==0.11.2
uv pip install Pillow==10.1.0
uv pip install uvicorn[standard]==0.24.0
uv pip install gunicorn==21.2.0
uv pip install psycopg2-binary==2.9.9
uv pip install django-crispy-forms==2.1
uv pip install crispy-tailwind==1.0.3
uv pip install whitenoise==6.6.0
echo "✅ Python dependencies installed"
echo ""

# Step 4: Install Node dependencies
echo "🎨 Step 4/7: Installing Tailwind CSS..."
npm install
echo "✅ Tailwind CSS installed"
echo ""

# Step 5: Build Tailwind
echo "🎨 Step 5/7: Building Tailwind CSS..."
npm run build
echo "✅ Tailwind CSS built"
echo ""

# Step 6: Create migrations
echo "🗄️  Step 6/7: Creating database migrations..."
uv run python manage.py makemigrations core
uv run python manage.py makemigrations universities
uv run python manage.py makemigrations programs
uv run python manage.py makemigrations students
uv run python manage.py makemigrations applications
echo "✅ Migrations created"
echo ""

# Step 7: Apply migrations
echo "🗄️  Step 7/7: Applying migrations..."
uv run python manage.py migrate
echo "✅ Database ready"
echo ""

echo "✅✅✅ SETUP COMPLETE! ✅✅✅"
echo ""
echo "📋 Next Steps:"
echo "1. Create superuser: uv run python manage.py createsuperuser"
echo "2. Run server: uv run python manage.py runserver"
echo "3. Visit: http://localhost:8000"
echo "4. Admin: http://localhost:8000/admin"
echo ""
echo "🎉 Happy coding!"
