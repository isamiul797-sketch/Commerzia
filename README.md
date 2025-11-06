🛍️ Commerzia

Commerzia is a full-featured Django-based e-commerce web application built with a modern, minimalistic design.
It allows users to browse laptops, view detailed product information, search for products, and securely make online payments through Stripe Checkout.

 Key Features
# Frontend

Clean, responsive Bootstrap 5 UI

Dynamic product listing with image, title, and discount price

Product detail pages for every laptop

Search functionality to find products easily

Multiple product sliders for featured and trending items

# Backend

Built using Django 5 and SQLite (default database)

Admin panel for managing products, categories, and orders

Integrated Stripe Payment Gateway for real transactions

Secure checkout flow (Customer → Payment → Order Confirmation)

Authentication system (Login, Logout, Registration, Profile Management)

# Stripe Payment Integration

Customers can select products and proceed to checkout

Payment session created using Stripe Checkout Session API

After successful payment, users are redirected to an order confirmation page

Orders are stored and displayed on the user’s order history page

# Search Functionality

Integrated live search system using Django query filters

Users can search laptops by name or description directly from the navigation bar

# Tech Stack

Backend: Django, SQLite

Frontend: HTML5, CSS3, Bootstrap 5

Payment: Stripe API

Authentication: Django Auth S

#How to Run Locally

1.Clone the repository:
git clone https://github.com/isamiul797-sketch/Commerzia.git

cd commerzia

2.Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate  # for Windows

3.Install dependencies:
pip install -r requirements.txt

4.Run database migrations:
python manage.py migrate

5.Start the server:
http://127.0.0.1:8000/

# Demo Flow

Browse products → Add to cart → Checkout

Secure payment via Stripe

Redirect to order confirmation page

View all past orders under My Orders

# Developer

Samiul Islam Sami

E-commerce & Django Developer

Focused on building scalable, secure backend systems with modern UI integration.

