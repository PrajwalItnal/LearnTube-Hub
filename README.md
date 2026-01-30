# 📺 LearnTube Hub  
### A YouTube-Powered E-Learning Platform built with Django

![Django](https://img.shields.io/badge/Django-6.0-darkgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

> **LearnTube Hub** is a lightweight Learning Management System (LMS) that allows users to publish, explore, and save **YouTube-based educational courses** with automatic video embedding.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [User Roles](#-user-roles)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [YouTube Embedding Logic](#-youtube-embedding-logic)
- [Limitations](#-limitations)
- [Future Enhancements](#-future-enhancements)
- [License](#-license)
- [Author](#-author)

---

## 🚀 Overview

**LearnTube Hub** is designed for learners and content creators who want a **simple and distraction-free platform** for sharing educational content hosted on YouTube.

✔ No certificates  
✔ No paid courses  
✔ Focused purely on learning & sharing  

---

## ✨ Features

- User authentication (Signup / Login / Logout)
- Role-based access (Student & Publisher)
- Publish YouTube-based courses
- Automatic YouTube link embedding
- Watch videos inside the platform
- Save courses using AJAX
- Responsive embedded video player

---

## 👥 User Roles

| Role | Capabilities |
|-----|-------------|
| Student | Browse, save & watch courses |
| Publisher | Upload & manage courses |
| Admin | Full control via Django Admin |

---

## 🗂 Project Structure

```text
LearnTube-Hub/
│
├── E_Learning/                # Project settings
│
├── users/                     # Main application
│   ├── migrations/
│   ├── templates/
│   │   └── users/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── static/
│   └── css/
│       ├── styles.css
│       ├── login.css
│       ├── signup.css
│       ├── profile.css
│       └── upload.css
│
├── templates/
│   └── base.html
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```
---

## 🧰 Technology Stack

| Technology | Purpose |
|:---|:---|
| **Python** | Backend logic |
| **Django 6.0** | Web framework |
| **SQLite** | Database |
| **HTML5** | Templates |
| **CSS3** | Styling |
| **JavaScript** | AJAX interactions |
| **Git & GitHub** | Version control |

---

## ⚙️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/PrajwalItnal/LearnTube-Hub.git
cd LearnTube-Hub
```
### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
```
### 3️⃣ Activate the Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```
**Linux / macOS:**
```bash
source venv/bin/activate
```
## 4️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
## 5️⃣ Apply Migrations
```bash
python manage.py migrate
```
## 6️⃣ Run the Development Server
```bash
python manage.py runserver
```
## 🌐 Open in Browser

Once the server is running, you can access the application at:

👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

### 🛠 Troubleshooting Connection
If the page doesn't load, ensure that:
1. Your virtual environment is still **activated**.
2. You have run the `python manage.py runserver` command without errors.
3. No other application is using port **8000**.

---

## 🔁 Usage

### 👨‍🏫 Publisher
* **Register / Login:** Create and manage your account.
* **Upload:** Simply paste YouTube course links.
* **Automatic Embedding:** Your courses are instantly ready for students.

### 👨‍🎓 Student
* **Register / Login:** Create your learning profile.
* **Browse:** Explore all available courses.
* **Save:** Keep your favorite courses in your library.
* **Watch:** Learn inside the platform or click through to YouTube.

---

## 📺 YouTube Embedding Logic

### ✅ Supported URLs
The platform supports standard and shortened YouTube links:
* `https://www.youtube.com/watch?v=VIDEO_ID`
* `https://youtu.be/VIDEO_ID`

### 🔄 Automatic Conversion
The system automatically converts links to the embed-friendly format:
* `https://www.youtube.com/embed/VIDEO_ID`

> [!CAUTION]
> **Note:** If a creator has disabled embedding, a "Watch on YouTube" fallback link is automatically displayed.

---

## ⚠️ Limitations
* No certification system currently available.
* No payment gateway integration.
* Restricted by YouTube's specific video embedding settings.

---

## 🚧 Future Enhancements
- [ ] **Search & Filters:** Find courses by keyword.
- [ ] **Organization:** Categories and tags for easier navigation.
- [ ] **Feedback:** Comments and star ratings.
- [ ] **Deployment:** Hosting on Render or Railway.
- [ ] **Database:** Transition to PostgreSQL support.

---

## 📄 License
This project is licensed under the **MIT License**.

---

## 👤 Contact

**Prajwal Itnal** *Computer Applications Student | Data Enthusiast*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/prajwal-itnal/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PrajwalItnal))
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:prajwalitnal20@gmail.com)

---
