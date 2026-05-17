# BusBook — Django Bus Ticket Booking System

A full-featured bus ticket booking web app converted from plain HTML/localStorage to **Django + SQLite ORM**.

---

## Project Structure

```
bus_ticket_booking/
├── manage.py
├── requirements.txt
├── db.sqlite3              ← auto-created on first run
├── bus_ticket_booking/     ← Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── booking/                ← Main Django app
    ├── models.py           ← All DB models (User, Bus, Booking, etc.)
    ├── views.py            ← Page views + JSON API endpoints
    ├── urls.py             ← URL routing
    ├── apps.py
    ├── migrations/
    │   └── 0001_initial.py
    ├── templates/booking/  ← All HTML templates
    │   ├── base.html
    │   ├── index.html
    │   ├── search.html
    │   ├── bus_detail.html
    │   ├── checkout.html
    │   ├── ticket.html
    │   ├── bookings.html
    │   ├── profile.html
    │   ├── login.html
    │   ├── register.html
    │   ├── admin_login.html
    │   └── admin.html
    └── static/booking/
        ├── css/style.css
        └── js/utils.js
```

---

## Setup & Run

### 1. Create & activate virtual environment
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply migrations (creates SQLite DB + tables)
```bash
python manage.py migrate
```

### 4. Run the development server
```bash
python manage.py runserver
```

### 5. Open in browser
```
http://127.0.0.1:8000/
```

---

## Pages & URLs

| URL | Description |
|-----|-------------|
| `/` | Home — search buses |
| `/search/?from=X&to=Y&date=Z` | Search results with filters |
| `/bus-detail/?busId=X&date=Y&from=A&to=B` | Seat selection |
| `/checkout/` | Passenger details + payment |
| `/ticket/?id=BKXXXXXXXX` | E-ticket view & print |
| `/bookings/` | My bookings (cancel, review) |
| `/profile/` | User profile & password change |
| `/login/` | User login (+ forgot password) |
| `/register/` | New user registration |
| `/admin-login/` | Admin login |
| `/admin-panel/` | Admin dashboard |

---

## Admin Credentials (seeded automatically)
- **Email:** admin@busbook.com  
- **Password:** admin123

---

## What Changed from the Original (localStorage → Django)

| Original | Django Version |
|----------|----------------|
| `localStorage` for all data | Django ORM + SQLite |
| `db.js` (fake database) | `models.py` (real models) |
| Session = localStorage `current_user` | Django `request.session` |
| `DB.searchBuses()` in JS | `views.py` → `Bus.objects.filter()` |
| `DB.saveBooking()` in JS | `views.py` → `Booking.objects.create()` |
| Static HTML files | Django templates with `{% %}` tags |
| No backend | Django views serve all pages + JSON APIs |

**UI, logic, and design are identical** — only the data layer was changed.

---

## Data Models

- **User** — name, email, phone, age, gender, password
- **Bus** — route, timing, price, seats, amenities, boarding/dropping points
- **BusReview** — linked to Bus, stores star ratings + comments
- **Booking** — links User + Bus, stores seat list, fare, payment, status
- **Passenger** — individual passenger per seat per booking
- **AdminUser** — separate admin credentials table
