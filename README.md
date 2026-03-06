Rent A`Cam - Camera Rental Platform

A Django-based camera rental management system that enables users to browse cameras, select rental dates, prevent overlapping bookings,
calculate dynamic pricing based on rental duration, and complete secure online payments.

Project Overview:
The system ensures accurate booking logic by validating availability at both frontend and backend levels.

Core Features:
#Authentication & User Management
#Registration & Login system
#OTP verification support
#Role-based access handling
#Cart & Wishlist System
#Review posting
#Online Payment & COD options

Tech Stack:
-Backend
#Django
#SQLite (Development)

-Frontend
#HTML
#Bootstrap
#JavaScript

-Third-Party Services
#Razorpay Payment Gateway
#Gmail SMTP (Email Service)
#Version Control
#Git
#GitHub

-Installation Guide
1️)Clone the Repository
git clone https://github.com/ajith-joshy/Rent-A-Cam---An-E-commercial-Website.git
cd camera-rental-platform

2)Create Virtual Environment
python -m venv venv
Activate:
Windows:
venv\Scripts\activate
Mac/Linux:
source venv/bin/activate

3️) Install Dependencies
pip install -r requirements.txt

4️)Configure Environment Variables
Create .env file:
SECRET_KEY=your_django_secret_key
EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_email_app_password
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret

5️) Run Migrations
python manage.py makemigrations
python manage.py migrate

6️) Start Development Server
python manage.py runserver
