@echo off
REM Install Django dan dependencies

echo Installing Django dan dependencies...
python -m pip install --upgrade pip
python -m pip install django==4.2
python -m pip install djangorestframework
python -m pip install djangorestframework-simplejwt
python -m pip install drf-spectacular
python -m pip install django-cors-headers
python -m pip install django-filter
python -m pip install python-decouple
python -m pip install pillow

echo.
echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo Langkah selanjutnya:
echo 1. python manage.py migrate
echo 2. python manage.py createsuperuser
echo 3. python manage.py runserver
echo.
pause
