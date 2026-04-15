# Smart Clinic Management System

Smart Clinic is a modern medical management platform designed to streamline interactions between patients, doctors, and administrative staff. Built with a focus on high-fidelity user experience and efficient clinical workflows, it offers a seamless interface for booking, record management, and real-time communication.

## System Architecture Overview

The system follows a modular **Model-View-Template (MVT)** architecture using the Django framework. Key design decisions include:

- **Decoupled Logic**: Business logic is separated into specialized packages (`views/`, `forms/`, `models/`) within each Django app (Users, Appointments, Records) for enhanced maintainability.
- **Role-Based Access Control (RBAC)**: A custom User model leverages Django's authentication system to enforce strict permission boundaries across the platform.
- **Glassmorphism UI**: High-fidelity frontend design using Vanilla CSS, optimized for both aesthetic appeal and readability.
- **Real-time Notifications**: An integrated notification system providing immediate feedback on account status and appointment changes.

## User Roles & Permissions

| Role | Permissions & Capabilities |
| :--- | :--- |
| **Patient** | Register account, book & manage appointments, view medical notes, manage personal profile (blood type, allergies, etc.). |
| **Doctor** | Manage clinical schedule, view patient details and appointment history, add medical notes. Requires Admin approval after registration. |
| **Admin** | Full system control: Approve/Reject doctor registrations, manage all staff/staff status, access global clinic bookings, and oversee patient directories. |

## Technology Stack

- **Backend**: Django 6.0.3 (Python 3.x)
- **Database**: SQLite (Development) / PostgreSQL (Production ready)
- **Frontend**: 
    - HTML5 & Semantic Tags
    - Vanilla CSS3 (Custom Glassmorphism Design System)
    - JavaScript (ES6+ for dynamic UI & AJAX/JSON integration)
- **Typography**: Google Fonts (Inter, Outfit)

## 🚀 Installation & Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/peerawattae/Smart_Clinic.git
   cd Smart_Clinic
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django pillow
   ```

4. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

## 💻 How to Run the System

1. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

2. **Access the application**:
   Open your browser and navigate to `http://127.0.0.1:8000/`

3. **Explore the Features**:
   - Register as a **Patient** to start booking.
   - Register as a **Doctor** and use the Admin account to approve your access via the **Admin Dashboard**.
   - Manage your information in the **My Profile** section.
