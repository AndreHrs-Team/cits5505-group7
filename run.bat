@echo off
call install.bat

call db_migration.bat

echo [Run] Activating virtual environment...
call .\application-env\Scripts\activate

echo [Run] Running Flask app...
flask run

pause