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

## 🗄️ Database Structure

The application uses an SQLite database to store information about foods, recipes, and meal plans. Below is the structure of the database:

### Tables

#### 1. `foods`
Stores information about individual food items.

| Column   | Type   | Description                     |
|----------|--------|---------------------------------|
| `id`     | INTEGER (Primary Key) | Unique identifier for each food item. |
| `name`   | TEXT   | Name of the food item.          |
| `calories` | REAL | Calories per serving.           |
| `protein` | REAL  | Protein content per serving (grams). |
| `carbs`   | REAL  | Carbohydrate content per serving (grams). |
| `fat`     | REAL  | Fat content per serving (grams). |
| `fiber`   | REAL  | Fiber content per serving (grams). |

#### 2. `recipes`
Stores information about recipes.

| Column   | Type   | Description                     |
|----------|--------|---------------------------------|
| `id`     | INTEGER (Primary Key) | Unique identifier for each recipe. |
| `name`   | TEXT   | Name of the recipe.             |

#### 3. `recipe_items`
Stores the relationship between recipes and the foods they contain, along with the quantity of each food item used in the recipe.

| Column       | Type   | Description                     |
|--------------|--------|---------------------------------|
| `id`         | INTEGER (Primary Key) | Unique identifier for each recipe item. |
| `recipe_id`  | INTEGER | Foreign key referencing `recipes(id)`. |
| `food_id`    | INTEGER | Foreign key referencing `foods(id)`. |
| `quantity`   | REAL    | Quantity of the food item used in the recipe. |

#### 4. `meal_plans`
Stores information about meal plans, including the date, meal type, and associated recipe.

| Column       | Type   | Description                     |
|--------------|--------|---------------------------------|
| `id`         | INTEGER (Primary Key) | Unique identifier for each meal plan. |
| `date`       | TEXT   | Date of the meal plan (e.g., `YYYY-MM-DD`). |
| `meal`       | TEXT   | Type of meal (e.g., breakfast, lunch, dinner). |
| `recipe_id`  | INTEGER | Foreign key referencing `recipes(id)`. |

### Relationships

- **`foods` ↔ `recipe_items`**: A food item can be part of multiple recipes, and a recipe can contain multiple food items.
- **`recipes` ↔ `meal_plans`**: A recipe can be part of multiple meal plans, and a meal plan references one recipe.

This structure allows the application to manage foods, recipes, and meal plans efficiently while maintaining data integrity through foreign key constraints.

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
