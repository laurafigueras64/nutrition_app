# 🥗 Nutrition Tracker Web App

A simple web-based application to manage foods, calculate macros, store recipes, and plan weekly meals using Python, Flask, and SQLite.

---

## 📦 Features

- Add and manage foods with macros (calories, protein, carbs, fat)
- Store recipes made from those foods
- View recipe macro summaries
- Calculate your theoretical macros
- Plan meals across the week

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/yourusername/nutrition-app.git
cd nutrition-app
```

### 2. Set Up a Virtual Environment

1. Create a virtual environment

    ```
    python -m venv env
    ```

    This will create a folder named `env` containing the virtual environment.

2. Activate the virtual environment

    - **Linux / macOS:**

        ```
        source env/bin/activate
        ```

    - **Windows (Command Prompt):**

        ```
        env\Scripts\activate
        ```

    - **Windows (PowerShell):**

        ```
        .\env\Scripts\Activate.ps1
        ```

3. Install dependencies. Make sure you have a `requirements.txt` file listing your Python dependencies. You can generate one with:

    ```
    pip freeze > requirements.txt
    ```

    Then run:

    ```
    pip install -r requirements.txt
    ```

### 3. Set Up the Database

Ensure the `db/` folder exists. Then run:

```
sqlite3 db/nutrition.db < schema.sql
```

If `sqlite3` is not installed, use your OS package manager (`apt`, `brew`, `choco`, etc.) or a GUI tool like DB Browser for SQLite.

### 4. Run the Application

```
python app.py
```

Then open your browser and go to:  
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🗂️ Project Structure

```
./
├── routes/
│   ├── __init__.py
│   ├── foods.py
│   ├── recipes.py
│   ├── planner.py
│   └── calculator.py
├── schema.sql
├── db/
│   └── nutrition.db
├── templates/
│   ├── index.html
│   ├── foods.html
│   ├── recipes.html
│   └── planner.html
├── static/
│   ├── style.css
│   └── script.js
├── venv/
├── README.md
└── requirements.txt
```


---

## 🧠 Dependencies

- Python 3.6+
- Flask
- SQLite3
- Jinja2 (template engine)
- Werkzeug (WSGI utility library)

---

## 🧹 Notes

- Uses raw SQL with SQLite for simplicity.
- Can be upgraded to PostgreSQL or MySQL easily.
- Logic and structure are designed to be simple and extensible.

---

## 📌 To-Do (Optional Features)

- User login system
- Dynamic macro calculator with live JS
- Weekly calendar planner interface
- Recipe import/export to JSON or CSV
