## CITS 5505 Agile Web Development (Group 7)
This is a repository for group 7 assignments

### Group Members
- Andre Harsono (24478126)
- Anqi Huang (23824496)
- Christina Fington (24260355)
- Steven Li (24291799)

---

# Student Assistant

Organize your student life with ease — all in one place.
Student Assistant is your personal tool for managing your academic schedule, financial habits, and fitness progress. Easily track your activities, gain meaningful insights, and share achievements with friends.

## Features
- **Education Calendar** - Import your class schedules from UWA Class Allocation System (CAS) and stay on top of your important dates
- **Finance Insight** - Track your income and expenses, visualize your spending patterns, and forecast your financial future
- **Fitness Tracker** - Record your daily activity and receive tailored health tips to stay active
- **Share Your Achievements** - Show off your top milestones by sharing your finance insights and fitness achievements with your peers

## Why Student Assistant?
- Simple, clean, and easy to use.
- Focused on what matters most for students: time, health, and money.
- Your data stays private — you choose what to share.

<div style="text-align: center;">
<h2>Study smart, spend smart, live smart.</h2>
</div>
---
## Technology Stack

- Backend: Flask with SQLAlchemy
- Database: SQLite
- Frontend: Bootstrap, jQuery, AJAX
- Data Visualization: Plotly.js
- File Parsing: Pandas, xmltodict

---
### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)
- Git
- [WeasyPrint](https://doc.courtbouillon.org/weasyprint/v62.0/first_steps.html) for PDF Report generation

For Windows, install the following packages before using WeasyPrint:
- MSYV2 [https://www.msys2.org/](https://www.msys2.org/) 
- GTK3-runtime – [https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases](https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer/releases)
Once installed, make sure GTK is added to your system's PATH.

On macOS, you can install WeasyPrint’s dependencies with Macports:
```bash
sudo port install py-pip pango libffi
```

### Preparations
1. Clone the repository:
```bash
git clone https://github.com/yourusername/healthtrack.git
cd healthtrack
```

2. Create a `.env` file in the project root with the following variables (adjust as needed):
```bash
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password

USE_AUTO_GENERATION=False

DATABASE_URL=sqlite:///dev.sqlite
```
> `USE_AUTO_GENERATION` is a flag that can be set to `True` or `False`. It controls whether the database is automatically created and seeded by the application on startup.
> This feature is only intended for **development purposes** or as a fallback when running `flask db migrate` is not possible.

> **⚠️ Important**: Auto generation is not compatible with > Flask-Migrate. Both mechanisms attempt to create and seed tables, > which can cause conflicts or duplication.
> You must choose either:
> -  Use Flask-Migrate (recommended): set `USE_AUTO_GENERATION=False`
> - Use auto-generation only: set `USE_AUTO_GENERATION=True`

> The provided run scripts from section [Running using provided script (Recommended)](#running-using-provided-script-recommended) use Flask-Migrate by default, so ensure `USE_AUTO_GENERATION=False` in that case.
Otherwise, the application may fail at startup.

> WARNING!!
> Never commit your `.env` to any version control (Git) as it may contains sensitive informations like passwords and API Keys.
> By default this repository have already ignored .env files so please refrain from adding it manually

3. Default admin and user account:
   - Email: admin@example.com
   - Password: admin@123
   - Email: user@example.com
   - Password: user@123

## Project Structure

- `app/`: Main application package
  - `models/`: Database models
  - `routes/`: Route blueprints
  - `services/`: Business logic
  - `static/`: CSS, JavaScript, and images
  - `utils/`: Helper functions
- `frontend/`: Frontend-specific assets
  - `static/`: CSS, JS, and image files
  - `templates/`: HTML or Jinja2 templates

## Database
The application is configured to use SQLite by default, with the database file stored in the `instance` folder. The code also have fallback to automatically create the database if it did not exists.

If you need to manually initialize or reset the database:
- Use `python -m app.init_db` to completely reset the database (drops all existing tables)
- Use `python -m app.init_db --create-only` to only create missing tables without losing data

## Running Instructions
- [Running using provided script (Recommended)](#running-using-provided-script-recommended)
  - [Running Steps (For Windows)](#running-steps-for-windows)
  - [Running Steps (For Mac and Linux)](#running-steps-for-mac-and-linux)
- [Manual Installation (For Windows)](#manual-installation-for-windows)
- [Manual Installation (For Mac and Linux)](#manual-installation-for-mac-and-linux)

## Running using provided script (Recommended)

> **Recommended:** Use `run.bat` (For Windows) or `run.sh` (For Linux or Mac) to automatically set up and run the project.

This script will:
- Check if the virtual environment `application-env` exists.
- Create the virtual environment if it does not exist.
- Install the required Python dependencies.
- Activate the virtual environment.
- Run the database migrations
- Start the backend server.
---

### Running Steps (For Windows)
1. Open Command Prompt (CMD) or PowerShell.
2. Navigate to the project root directory.
3. Execute:
```bat
./run.bat
```

---
### Running Steps (For Mac and Linux)

1. Open Terminal.
2. Navigate to the project root directory.
3. Execute:

```bash
./run.sh
```

> If you encounter a "Permission Denied" error, grant execute permission with the following command then try step 3 again.
>```bash
>chmod +x run.sh
>```
---

## Manual Installation (For Windows)

If you prefer to manually install and run the project:
1. Open Command Prompt (CMD) or PowerShell.
2. Navigate to the project root directory.
3. Create a Python virtual environment named `application-env`:

```bat
python -m venv application-env
```

4. Activate the virtual environment:

```bat
application-env\Scripts\activate
```

5. Install the required dependencies:

```bat
pip install -r requirements.txt
```

6. Run the database upgrade migration:

```bat
flask db upgrade
```

7. Run the Flask server:

```bat
flask run
```

---

## Manual Installation (For Mac and Linux)

If you prefer to manually install and run the project:

1. Open Terminal.
2. Navigate to the project root directory.
3. Create a Python virtual environment named `application-env`:

```bash
python3 -m venv application-env
```

4. Activate the virtual environment:

```bash
source application-env/bin/activate
```

5. Install the required dependencies:

```bash
pip install -r requirements.txt
```

6. Run the database upgrade migration:

```bat
flask db upgrade
```

7. Run the Flask server:

```bash
flask run
```

---

> **Note:** The executable permissions for `.sh` scripts (`install.sh`, `run.sh`, `dev_run.sh`) are already set in the repository. However, if you encounter any permission issues on your system, please use the following command to fix it:
>
> ```bash
> chmod +x *.sh
> ```
>
> This will ensure all the helper scripts are executable.


## License

This project is licensed under the MIT License - see the LICENSE file for details.