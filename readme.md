## CITS 5505 Agile Web Development (Group 7)
This is a repository for group 7 assignments

### Group Members
- Andre Harsono (24478126)
- Anqi Huang (23824496)
- Christina Fington (24260355)
- Steven Li (24291799)

For tickets and logs please check projects tab instead

## Running Instructions
- [Running Steps (For Windows)](#running-using-provided-script-recommended)
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

6. Navigate to the `backend` directory:

```bat
cd backend
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

6. Navigate to the `backend` directory:

```bash
cd backend
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
