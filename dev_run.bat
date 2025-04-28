@echo off
call install.bat

echo Moving into backend folder...
cd backend

echo Activating virtual environment...
call ..\application-env\Scripts\activate.bat

echo Running Flask app...
python app.py

pause