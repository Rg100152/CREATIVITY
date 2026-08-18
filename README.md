

# 🎨 CREATIVITY
### *Artistic Portfolio & Surreal Event Platform*

A sleek, dark-themed, single-file Flask web application built with surreal CSS artwork, interactive galleries, live animated counters, and asynchronous event booking.

[![GitHub Repo](https://img.shields.io/badge/Repository-Rg100152%2FCREATIVITY-e2a76f?style=for-the-badge&logo=github)](https://github.com/Rg100152/CREATIVITY)
[![Python Version](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Flask Framework](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![SQLite3](https://img.shields.io/badge/Database-SQLite3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<br />

[View Demo](https://github.com/Rg100152/CREATIVITY) • [Report Bug](https://github.com/Rg100152/CREATIVITY/issues) • [Request Feature](https://github.com/Rg100152/CREATIVITY/issues)

</div>

---

## 🌌 Overview

**CREATIVITY** is an all-in-one artistic exhibition and event booking platform. Built as an ultra-clean, production-ready single-file Flask application, it combines dark minimalist aesthetics with pure CSS animations, asynchronous AJAX endpoints, and dynamic SQLite data persistence.

---

## ✨ Key Features

* 🪐 **Pure CSS Surreal Artwork:** Floating cloud head, orbital rings, and dynamic animated space particles without heavy external canvas libraries.
* 🖼️ **Dynamic Art Gallery & Lightbox:** Artwork dynamically rendered from SQLite with smooth modal inspection.
* 🎟️ **Asynchronous Ticket Booking:** Seamless, page-reload-free modal booking system backed by AJAX endpoints.
* 📊 **Intersection Observer Counters:** Smooth statistics and milestones animation triggered on viewport entry.
* 📬 **Contact Form Integration:** Asynchronous contact messaging pipeline with validation feedback.
* ⚡ **Zero-Config Database Engine:** Automatic schema creation and pre-seeded curated artwork on first boot.

---

## 🛠️ Tech Stack

| Component | Technologies Used |
| :--- | :--- |
| **Backend** | Python 3, Flask |
| **Database** | SQLite3 |
| **Frontend** | HTML5, CSS3 (Custom Keyframe Animations, Glassmorphism, CSS Grid & Flexbox) |
| **Scripting** | Vanilla JavaScript (ES6+, Fetch API, IntersectionObserver) |

---

## 📁 Project Structure

```plaintext
CREATIVITY/
│
├── app.py              # Core application (Backend, Database Models, HTML/CSS/JS)
├── creativity.db       # Auto-generated SQLite Database
├── requirements.txt    # Project dependencies
└── README.md           # Documentation

🚀 Quick Start Guide
1. Clone the Repository
git clone [https://github.com/Rg100152/CREATIVITY.git](https://github.com/Rg100152/CREATIVITY.git)
cd CREATIVITY

2. Create and Activate Virtual Environment
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

3. Install Dependencies
pip install flask

(Or pip install -r requirements.txt if available)
4. Run the Application
python3 app.py

Open your browser and navigate to:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

📡 API Endpoints
| Method | Endpoint | Description | Payload |
|---|---|---|---|
| GET | / | Renders the primary portfolio interface | None |
| POST | /api/book | Processes event ticket reservations | name, email, tickets |
| POST | /api/contact | Handles direct inquiries & feedback | name, email, message |
🗄️ Database Schema
-- Artworks Table
CREATE TABLE gallery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT NOT NULL
);

-- Ticket Bookings Table
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    tickets INTEGER NOT NULL,
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Contact Messages Table
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

👨‍💻 Author
Raj Gautam
 * GitHub: @Rg100152
 * Project Repository: CREATIVITY
📄 License
This project is licensed under the MIT License — feel free to use, modify, and distribute it for personal and educational projects.

