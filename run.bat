@echo off
call install.bat

@REM echo Moving into backend folder...
@REM cd backend

echo Activating virtual environment...
call ..\application-env\Scripts\activate.bat

echo Running Flask app...
flask run

pause