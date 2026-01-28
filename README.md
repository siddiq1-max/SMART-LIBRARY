# 📚 Smart Library Management System

A modern, full-stack library management application built with **Flask** (Python). Features a "BookMyShow" style discovery interface, user marketplace, and comprehensive admin/librarian tools.

**Designed & Developed by [Siddiq]**

![Smart Library](https://images.unsplash.com/photo-1507842217343-583bb7270b66?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80)

## 🚀 Key Features

### For Users
*   **Modern Discovery**: Browse books with cinematic carousels, categories, and "BookMyShow" style details.
*   **User Marketplace**: Sell your own used books to other members.
*   **Wallet System**: Earn money from sales and track your balance.
*   **Dashboard**: Manage loans, reservations, and purchase history.
*   **Smart Search**: Filter by category, author, or title.

### For Librarians & Admins
*   **Book Management**: Add, edit, and remove library inventory.
*   **Transaction Handling**: Issue and return books with due date tracking.
*   **Sales Reports**: Track revenue from book sales.
*   **User Management**: Control user access and roles.

## 🛠️ Tech Stack
*   **Backend**: Python, Flask, SQLAlchemy, Flask-Login
*   **Database**: SQLite (Dev) / PostgreSQL (Prod)
*   **Frontend**: HTML5, Bootstrap 5, CSS3 (Glassmorphism), JavaScript
*   **Hosting Ready**: Configured for Render.com

## 📦 Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone https://github.com/siddiq1-max/SMART-LIBRARY.git
    cd SMART-LIBRARY
    ```

2.  **Create Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize Database**
    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    python seed_data.py  # (Optional) Seed with sample data
    ```

5.  **Run Application**
    ```bash
    python run.py
    ```
    Visit `http://127.0.0.1:5000` in your browser.

## ☁️ Deployment

This project is configured for deployment on **Render.com**.
See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
