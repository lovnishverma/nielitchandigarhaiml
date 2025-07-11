# 📚 AI-ML Topics Management Portal (Flask-Based)

A full-featured Flask web application with user registration, login/logout, admin panel, topic management system, and session-based visitor tracking. The admin can manage users and upload AI/ML-related topics with images and PDF links.

> 🔗 **Live URL**: [https://nielitchandigarhaiml.onrender.com](https://nielitchandigarhaiml.onrender.com)

---

## ✨ Features

- ✅ User Registration & Login (with hashed passwords)
- 🔒 Role-Based Access (admin panel)
- 🧠 AI/ML Topics Listing (image + name + description + PDF)
- ➕ Add/Edit/Delete Topics (admin only)
- 📈 Visitor Counter (session-aware)
- 📅 Indian Timezone Timestamp with greeting
- 👥 Admin can list and delete users (except self)
- 🧰 SQLite Database Integration
- 📄 Clean and modern templated UI (using Jinja2 templates)

---

## 🏗️ Tech Stack

- **Backend**: Flask (Python), Flask-Login, Flask-SQLAlchemy
- **Frontend**: HTML5, CSS3, Bootstrap (optional), Jinja2
- **Database**: SQLite
- **Deployment**: [Render.com](https://render.com)

---

## 🗂️ Project Structure

```

project/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── main.html
│   ├── user\_list.html
│   ├── admin\_panel.html
│   ├── add\_topic.html
│   ├── modify\_topic.html
│   ├── list\_topics.html
│
├── static/
│   └── (CSS/JS/Images - optional)
│
├── visitor\_count.txt
├── database.db
├── app.py
├── requirements.txt
└── README.md

````

---

## 🚀 Installation Guide

1. **Clone the repository**

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
````

2. **Create a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Create database and visitor file**

```bash
# Create SQLite database
python
>>> from app import db
>>> db.create_all()
>>> exit()

# Create visitor counter file
echo "0" > visitor_count.txt
```

5. **Run the Flask app**

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

---

## 🔑 Admin Access

* **Username:** `admin`
* **Note:** First create the admin user manually or register as `admin`.

---

## 📝 Environment Variables (optional)

You may also move secrets to an `.env` file:

```env
SECRET_KEY=ab#1867$@817
DATABASE_URL=sqlite:///database.db
```

Then load them in `app.py` using `python-dotenv`.

---

## 📸 Screenshots

| Login Page                           | Dashboard                                    | Admin Panel                                |
| ------------------------------------ | -------------------------------------------- | ------------------------------------------ |
| ![Login](docs/screenshots/login.png) | ![Dashboard](docs/screenshots/dashboard.png) | ![Admin](docs/screenshots/admin_panel.png) |

*(Add screenshots to `docs/screenshots/` folder and update above)*

---

## 🧪 Routes Overview

| Route                      | Method   | Description                 |
| -------------------------- | -------- | --------------------------- |
| `/login`                   | GET/POST | Login form                  |
| `/register`                | GET/POST | Register new user           |
| `/logout`                  | GET      | Logout current user         |
| `/`                        | GET      | Dashboard (requires login)  |
| `/admin`                   | GET      | Admin home panel            |
| `/admin/add_topic`         | GET/POST | Add new topic               |
| `/admin/list_topics`       | GET      | List all topics             |
| `/admin/modify_topic/<id>` | GET/POST | Edit topic                  |
| `/admin/delete_topic/<id>` | POST     | Delete topic                |
| `/users`                   | GET      | List all users (admin only) |
| `/delete_user/<id>`        | POST     | Delete user (admin only)    |

---

## 🛡️ Security Notes

* Passwords are securely hashed using Werkzeug.
* Only authenticated users can access the dashboard.
* Admin-specific routes are protected by username checks.
* Users can't delete themselves.

---

## 📬 Contact / Contribution

Feel free to open issues or pull requests for improvements.

> Built by [Lovnish Verma](https://lovnishverma.github.io/)
> Deployment: [https://nielitchandigarhaiml.onrender.com](https://nielitchandigarhaiml.onrender.com)

---

## 📃 License

This project is open-source and free to use under the [MIT License](LICENSE).


---
