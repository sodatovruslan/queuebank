# QueueBank 🏦

Electronic queue management system for banks built with Django.

## Features
- 🎟️ Take tickets for bank services
- 🖥️ Operator panel to manage queue
- 👑 Admin dashboard with statistics
- 🤖 AI Assistant powered by Groq
- 📧 Email confirmation on register
- 🔐 Role-based permissions

## Roles
- **Client** — take tickets, view queue
- **Operator** — manage queue, call clients
- **Admin** — full access, dashboard

## Installation
```bash
git clone https://github.com/sodatovruslan/queuebank.git
cd queuebank
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Tech Stack
- Python 3.14
- Django 6.0
- SQLite
- Groq AI (llama-3.3-70b)