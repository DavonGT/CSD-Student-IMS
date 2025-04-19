# CSD Student IMS

## Overview
CSD Student IMS (Information Management System) is a Django-based web application designed to efficiently manage student information. It leverages the Django framework alongside HTML, CSS, and JavaScript to provide an intuitive and responsive user interface.

---

## Features
- **Student Records Management**: Add, update, delete, and view student records.
- **User Authentication**: Secure login and registration system with Django's built-in authentication.
- **Interactive Dashboard**: Visualize student data and analytics.
- **Responsive Design**: Optimized for both desktop and mobile devices.

---

## Installation and Setup

### Prerequisites
Ensure you have the following installed on your system:
- Python (version 3.8 or higher)
- Django (version 3.0 or higher)
- A virtual environment tool (e.g., `venv` or `virtualenv`)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/DavonGT/CSD-Student-IMS.git
   cd CSD-Student-IMS
   ```

2. Set up the virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser to access the admin panel:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Open your web browser and navigate to:
   ```
   http://127.0.0.1:8000
   ```

---
