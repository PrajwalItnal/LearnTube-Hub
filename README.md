# 📺 LearnTube Hub  
### A Modern, YouTube-Powered E-Learning Platform built with Django

![Django](https://img.shields.io/badge/Django-6.0-darkgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Architecture](https://img.shields.io/badge/Architecture-Service--Layer-orange)
![UI](https://img.shields.io/badge/UI-Coursera--Style-blue)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)

> **LearnTube Hub** is a premium Learning Management System (LMS) designed to mirror the professional feel of platforms like Coursera. It allows users to build, explore, and track progress through **YouTube-powered courses** organized into modules and lessons.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Key Features](#-key-features)
- [Evolution (Model Upgrade)](#-evolution-model-upgrade)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Docker Deployment](#-docker-deployment)
- [License](#-license)

---

## 🚀 Overview

LearnTube Hub has been upgraded from a simple video-sharing tool into a **robust educational platform**. It features a service-oriented backend architecture and a glassmorphic, responsive sidebar-based UI.

✔ **Sleek Coursera-Style UI**: Modern dashboard, persistent sidebar, and glassmorphic accents.  
✔ **Advanced Progress Tracking**: Real-time YouTube watch-time syncing and "resume where you left off" logic.  
✔ **Multi-Module Courses**: Support for Lessons, Modules, and structured curriculum.  
✔ **Verified Certificates**: Automated generation with unique IDs and QR code verification.  

---

## 🏗 System Architecture

The project now follows a strict **Clean Architecture** pattern by separating business logic from views:

- **Views layer**: Handles HTTP requests and template rendering.
- **Service layer (`services.py`)**: Contains core logic for enrollments, progress tracking, and validation.
- **Models layer**: Structured to handle complex course hierarchies.

---

## 🧬 Evolution (Model Upgrade)

We transitioned from a single-video model to a hierarchical structure:
1. **Course**: The main container.
2. **Module**: Logical chapters within a course.
3. **Lesson**: individual videos/content items within modules.

*Legacy courses were automatically migrated into an "Introduction" module during the upgrade.*

---

## 🧰 Technology Stack

| Category | Technology |
|:---|:---|
| **Backend** | Python, Django 6.0 |
| **Logic Layer** | Custom Service-Layer Architecture |
| **Database** | SQLite (compatible with PostgreSQL via dj-database-url) |
| **Frontend** | Vanilla CSS (Modern Design Tokens, Glassmorphism), JavaScript (YouTube Iframe API) |
| **DevOps** | Docker, Docker Compose, python-dotenv |

---

## ⚙️ Installation

### 1️⃣ Clone & Setup
```bash
git clone https://github.com/PrajwalItnal/LearnTube-Hub.git
cd LearnTube-Hub
python -m venv venv
# Activate venv (Windows: venv\Scripts\activate | Mac/Linux: source venv/bin/activate)
```

### 2️⃣ Configure Environment
Create a `.env` file (see `.env.example`):
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 3️⃣ Install & Migrate
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

---

## 🐳 Docker Deployment

The project is fully dockerized for production-ready deployment:

```bash
docker-compose up --build
```

---

## 📄 License
This project is licensed under the **MIT License**.

---

## 👤 Author
**Prajwal Itnal**  
*Computer Applications Student | Data Enthusiast*
