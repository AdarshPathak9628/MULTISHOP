# MULTISHOP

E-Commerce Website built with Django, MySQL, Bootstrap

# 🛒 MultiShop — E-Commerce Website

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Django](https://img.shields.io/badge/Django-6.0-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

> A full-featured e-commerce website built with Django, MySQL, Bootstrap 5

---

## 👨‍💻 Developer

**Adarsh Pathak**
GitHub: [@AdarshPathak9628](https://github.com/AdarshPathak9628)

---

## 🌟 Features

### Customer Features

- ✅ User Registration & Login
- ✅ Browse Products by Category
- ✅ Search & Filter Products
- ✅ Shopping Cart (Add/Remove/Update)
- ✅ Checkout with Billing Address
- ✅ Order Placement
- ✅ User Profile

### Admin Features

- ✅ Admin Dashboard
- ✅ Manage Products
- ✅ Manage Categories
- ✅ Manage Orders
- ✅ Manage Vendors
- ✅ Manage Customers

---

## 🛠️ Tech Stack

| Technology   | Version | Purpose          |
| ------------ | ------- | ---------------- |
| Python       | 3.13    | Backend Language |
| Django       | 6.0     | Web Framework    |
| MySQL        | 8.0     | Database         |
| Bootstrap    | 5.3     | Frontend Styling |
| HTML/CSS     | 5/3     | Templates        |
| JavaScript   | ES6     | Interactivity    |
| Font Awesome | 6.4     | Icons            |

---

## 📁 Project Structure

```
MULTISHOP/
│
├── multishop_project/     # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── store/                 # Main app
│   ├── models.py          # Database tables
│   ├── views.py           # Page logic
│   ├── urls.py            # URL routing
│   └── admin.py           # Admin panel
│
├── templates/
│   ├── store/             # Customer pages
│   └── dashboard/         # Admin pages
│
├── static/                # CSS, JS, Images
├── media/                 # Uploaded files
├── requirements.txt       # Dependencies
└── manage.py
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/AdarshPathak9628/MULTISHOP.git
cd MULTISHOP
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create MySQL Database

```sql
CREATE DATABASE multishop_db CHARACTER SET utf8mb4;
```

### 5. Configure Database in `settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'multishop_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create Admin User

```bash
python manage.py createsuperuser
```

### 8. Run Server

```bash
python manage.py runserver
```

### 9. Open Browser

```
http://127.0.0.1:8000/
```

---

## 📊 Database Models

| Model          | Description         |
| -------------- | ------------------- |
| Category       | Product categories  |
| Product        | All products        |
| Vendor         | Sellers/vendors     |
| Cart           | Shopping cart items |
| Order          | Customer orders     |
| OrderItem      | Items inside orders |
| BillingAddress | Delivery addresses  |
| Profile        | User profiles       |

---

## 🔑 Admin Panel

```
URL: http://127.0.0.1:8000/admin/
```

---

## 📝 License

This project is for educational purposes.
