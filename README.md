Faculty Course Management Web Application

A Django web application developed as a student project for managing students, professors, courses, and university enrollments.



Features

User authentication (sign up, sign in, and sign out)



Role-based access control (Administrator, Professor, and Student)



Student and professor profile management



Course creation and editing



Course assignment to professors



Overview of enrolled courses



Course enrollment and removal



Tracking of passed courses and academic course signatures (potpisi)



Roster overview of students enrolled in specific courses



Technologies

Python



Django 4.2



SQLite



HTML templates



Git and GitHub



Getting Started

1\. Clone the Repository

git clone https://github.com/martinavukojevic/web\_aplikacija.git

cd web\_aplikacija



2\. Create a Virtual Environment

python -m venv .venv



Activation on Windows (PowerShell):



.\\.venv\\Scripts\\Activate.ps1



3\. Install Dependencies

python -m pip install -r .\\seminar\\requirements.txt



4\. Configure the Secret Key

Before running the application, you must set the DJANGO\_SECRET\_KEY environment variable.



Example for PowerShell:



$env:DJANGO\_SECRET\_KEY = python -c "import secrets; print(secrets.token\_urlsafe(50))"



Note: This command sets the key for the current PowerShell session only.



5\. Run Database Migrations

python .\\seminar\\manage.py migrate



6\. Run the Development Server

python .\\seminar\\manage.py runserver



The application will be accessible at http://127.0.0.1:8000/.



Disclaimer

This project was developed for educational purposes. For production use, security settings and application configurations must be thoroughly reviewed and hardened.
