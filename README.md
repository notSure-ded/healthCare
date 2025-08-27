# Healthcare Backend API

## Objective
This project is a robust backend system for a healthcare application, built using Django and Django REST Framework. The system provides a secure, scalable foundation for managing users, patients, and doctors, with a complete set of RESTful API endpoints and JWT-based authentication.

---

## Features
- **Secure User Authentication**: User registration and login system using JSON Web Tokens (JWT).
- **Patient Management**: Full CRUD (Create, Read, Update, Delete) functionality for patient records, accessible only by the user who created them.
- **Doctor Management**: Full CRUD functionality for doctor records.
- **Role-Based Permissions**: Only admin users (staff) can create, update, or delete doctor records. Regular authenticated users have read-only access.
- **Patient-Doctor Mapping**: System to assign doctors to patients and manage these relationships.
- **Custom User Model**: Uses email as the primary identifier for users instead of a username.
- **Admin Panel**: A customized Django admin interface for easy data management.
- **Validation & Error Handling**: Clear error messages for common issues like duplicate emails or invalid data.

---

## Tech Stack
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: djangorestframework-simplejwt
- **Environment Variables**: python-decouple

---

## Setup and Installation

Follow these steps to get the project running locally.

### 1. Prerequisites
- Python 3.8+
- PostgreSQL installed and running.
- A virtual environment tool (`venv`).

### 2. Clone & Setup
```bash
# Clone the repository (conceptual)
# git clone <your-repo-url>
# cd <project-folder>

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
Install all required packages using the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project's root directory. Copy the contents of `.env.example` and fill in your database credentials and a secret key.

**.env file:**
```ini
SECRET_KEY='your-strong-secret-key-here'
DEBUG=True

DB_NAME='your_db_name'
DB_USER='your_db_user'
DB_PASSWORD='your_db_password'
DB_HOST='localhost'
DB_PORT='5432'
```

### 5. Run Database Migrations
Apply the database schema and create the necessary tables.
```bash
python manage.py makemigrations api
python manage.py migrate
```

### 6. Create a Superuser
This account will have admin privileges and access to the Django Admin Panel.
```bash
python manage.py createsuperuser
```
Follow the prompts to set up your admin email and password.

### 7. Run the Server
Start the development server.
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

---

## API Endpoints Guide

Base URL: `http://127.0.0.1:8000`

### 1. Authentication

#### `POST /api/auth/register/`
- **Description**: Registers a new user.
- **Body**:
  ```json
  {
      "name": "Your Name",
      "email": "user@example.com",
      "password": "yourpassword"
  }
  ```

#### `POST /api/auth/login/`
- **Description**: Logs in a user and returns JWT access and refresh tokens.
- **Body**:
  ```json
  {
      "email": "user@example.com",
      "password": "yourpassword"
  }
  ```
- **Response**:
  ```json
  {
      "refresh": "...",
      "access": "..."
  }
  ```

---
### 2. Patient Management
**Authentication**: Requires `Bearer <access_token>` in the `Authorization` header for all endpoints.

#### `POST /api/patients/`
- **Description**: Adds a new patient. The patient is automatically linked to the logged-in user.

#### `GET /api/patients/`
- **Description**: Retrieves a list of all patients created by the authenticated user.

#### `GET /api/patients/<id>/`
- **Description**: Retrieves details of a specific patient.

#### `PUT /api/patients/<id>/`
- **Description**: Updates the details of a specific patient.

#### `DELETE /api/patients/<id>/`
- **Description**: Deletes a patient record.

---
### 3. Doctor Management
**Authentication**: Requires `Bearer <access_token>` in the `Authorization` header.

#### `POST /api/doctors/`
- **Description**: Adds a new doctor. **(Admin/Staff only)**

#### `GET /api/doctors/`
- **Description**: Retrieves a list of all doctors. **(All authenticated users)**

#### `GET /api/doctors/<id>/`
- **Description**: Retrieves details of a specific doctor. **(All authenticated users)**

#### `PUT /api/doctors/<id>/`
- **Description**: Updates the details of a specific doctor. **(Admin/Staff only)**

#### `DELETE /api/doctors/<id>/`
- **Description**: Deletes a doctor record. **(Admin/Staff only)**

---
### 4. Patient-Doctor Mapping
**Authentication**: Requires `Bearer <access_token>` in the `Authorization` header.

#### `POST /api/mappings/`
- **Description**: Assigns a doctor to one of the user's patients.
- **Body**:
  ```json
  {
      "patient_id": 1,
      "doctor_id": 1
  }
  ```

#### `GET /api/mappings/`
- **Description**: Retrieves all patient-doctor mappings.

#### `GET /api/mappings/<patient_id>/`
- **Description**: Gets all doctors assigned to a specific patient.

#### `DELETE /api/mappings/delete/<id>/`
- **Description**: Removes a specific patient-doctor mapping by its ID.
