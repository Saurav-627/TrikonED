#!/bin/bash
# TrikonED Setup Script - Automated Django Project Setup with UV

echo "🚀 TrikonED Setup Script"
echo "========================"

# Install UV if not already installed
echo "📦 Installing UV package manager..."
pip install uv

# Create virtual environment with UV
echo "🔧 Creating virtual environment..."
uv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source .venv/bin/activate

# Install Django and dependencies with UV
echo "📥 Installing dependencies with UV..."
uv pip install Django==4.2.8
uv pip install django-environ==0.11.2
uv pip install Pillow==10.1.0
uv pip install uvicorn[standard]==0.24.0
uv pip install gunicorn==21.2.0
uv pip install psycopg2-binary==2.9.9
uv pip install django-crispy-forms==2.1
uv pip install crispy-tailwind==1.0.3
uv pip install whitenoise==6.6.0

# Install Tailwind dependencies
echo "🎨 Installing Tailwind CSS..."
npm install

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source .venv/bin/activate"
echo "2. Run migrations: uv run python manage.py migrate"
echo "3. Create superuser: uv run python manage.py createsuperuser"
echo "4. Build Tailwind: npm run build"
echo "5. Run server: uv run python manage.py runserver"
echo ""
