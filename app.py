from flask import Flask, render_template, request, redirect
import sqlite3
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)

# Set up logging
if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=5)
file_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
))
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Nutrition Tracker startup')

DB_PATH = 'db/nutrition.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def get_number_or_zero(field):
    value = request.form.get(field, '').strip()
    return float(value) if value else 0.0

@app.route('/')
def index():
    app.logger.info("Visited home page")
    return render_template('index.html')

# ----------------------
# FOOD MANAGEMENT
# ----------------------
@app.route('/foods', methods=['GET', 'POST'])
def foods():
    conn = get_db()
    if request.method == 'POST':
        try:
            name = request.form['name']
            calories = get_number_or_zero('calories')
            protein = get_number_or_zero('protein')
            carbs = get_number_or_zero('carbs')
            fat = get_number_or_zero('fat')
            fiber = get_number_or_zero('fiber')
            conn.execute("""
                INSERT INTO foods (name, calories, protein, carbs, fat, fiber)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (name, calories, protein, carbs, fat, fiber)
            )
            conn.commit()
            app.logger.info(f"Added food: {name}")
        except Exception as e:
            app.logger.error(f"Error adding food: {e}")
        return redirect('/foods')
    
    foods = conn.execute("SELECT * FROM foods").fetchall()
    app.logger.info("Displayed food list")
    return render_template('foods.html', foods=foods)

# ----------------------
# RECIPE MANAGEMENT
# ----------------------
@app.route('/recipes', methods=['GET', 'POST'])
def recipes():
    conn = get_db()
    if request.method == 'POST':
        try:
            recipe_name = request.form['recipe_name']
            food_id = int(request.form['food_id'])
            quantity = float(request.form['quantity'])

            recipe = conn.execute("SELECT id FROM recipes WHERE name = ?", (recipe_name,)).fetchone()
            if not recipe:
                conn.execute("INSERT INTO recipes (name) VALUES (?)", (recipe_name,))
                conn.commit()
                app.logger.info(f"Created new recipe: {recipe_name}")
                recipe_id = conn.execute("SELECT id FROM recipes WHERE name = ?", (recipe_name,)).fetchone()['id']
            else:
                recipe_id = recipe['id']

            conn.execute("""
                INSERT INTO recipe_items (recipe_id, food_id, quantity)
                VALUES (?, ?, ?)""",
                (recipe_id, food_id, quantity)
            )
            conn.commit()
            app.logger.info(f"Added food ID {food_id} to recipe '{recipe_name}' (qty: {quantity}g)")
        except Exception as e:
            app.logger.error(f"Error updating recipe: {e}")
        return redirect('/recipes')

    foods = conn.execute("SELECT * FROM foods").fetchall()
    recipe_rows = conn.execute("SELECT * FROM recipes").fetchall()
    recipes = []

    for recipe in recipe_rows:
        items = conn.execute("""
            SELECT fi.quantity, f.calories, f.protein, f.carbs, f.fat
            FROM recipe_items fi
            JOIN foods f ON fi.food_id = f.id
            WHERE fi.recipe_id = ?""", (recipe['id'],)).fetchall()

        total_cals = sum(item['calories'] * item['quantity'] / 100 for item in items)
        total_prot = sum(item['protein'] * item['quantity'] / 100 for item in items)
        total_carb = sum(item['carbs'] * item['quantity'] / 100 for item in items)
        total_fat = sum(item['fat'] * item['quantity'] / 100 for item in items)

        recipes.append({
            'name': recipe['name'],
            'calories': round(total_cals, 1),
            'protein': round(total_prot, 1),
            'carbs': round(total_carb, 1),
            'fat': round(total_fat, 1)
        })

    app.logger.info("Displayed recipe list")
    return render_template('recipes.html', foods=foods, recipes=recipes)

# ----------------------
# MEAL PLANNER
# ----------------------
@app.route('/planner', methods=['GET', 'POST'])
def planner():
    conn = get_db()
    if request.method == 'POST':
        try:
            date = request.form['date']
            meal = request.form['meal']
            recipe_id = request.form['recipe_id']
            conn.execute("""
                INSERT INTO meal_plans (date, meal, recipe_id)
                VALUES (?, ?, ?)""", (date, meal, recipe_id))
            conn.commit()
            app.logger.info(f"Planned meal '{meal}' on {date} using recipe ID {recipe_id}")
        except Exception as e:
            app.logger.error(f"Error adding meal plan: {e}")
        return redirect('/planner')

    recipes = conn.execute("SELECT * FROM recipes").fetchall()
    plans = conn.execute("""
        SELECT mp.date, mp.meal, r.name AS recipe_name
        FROM meal_plans mp
        JOIN recipes r ON mp.recipe_id = r.id
        ORDER BY mp.date
    """).fetchall()
    app.logger.info("Displayed meal planner")
    return render_template('planner.html', recipes=recipes, plans=plans)

# ----------------------
# CALCULATOR
# ----------------------
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    macros = None
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            weight = float(request.form['weight'])  # in kg
            height = float(request.form['height'])  # in cm
            gender = request.form['gender']
            activity = float(request.form['activity'])  # multiplier
            goal = request.form['goal']  # 'lose', 'maintain', or 'gain'
            body_fat = float(request.form['body_fat']) / 100  # convert to decimal

            # Step 1: Lean Body Mass (kg)
            lbm = weight * (1 - body_fat)

            # Step 2: BMR (Mifflin-St Jeor)
            if gender == 'male':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

            # Step 3: Maintenance Calories
            maintenance = bmr * activity

            # Step 4: Adjust Calories for Goal
            if goal == 'lose':
                calories = maintenance * 0.80
            elif goal == 'gain':
                calories = maintenance * 1.10
            else:
                calories = maintenance

            # Step 5: Protein per kg LBM
            if body_fat <= 0.22:
                protein_per_kg = 3.3
            elif body_fat <= 0.28:
                protein_per_kg = 3.0
            else:
                protein_per_kg = 2.6

            protein = round(protein_per_kg * lbm)
            protein_cal = protein * 4

            # Step 6: Fat as % of total calories
            if body_fat <= 0.22:
                fat_percent = 0.20
            elif body_fat <= 0.28:
                fat_percent = 0.25
            else:
                fat_percent = 0.30

            fat_cal = calories * fat_percent
            fat = round(fat_cal / 9)

            # Step 7: Carbs = remaining calories
            carb_cal = calories - (protein_cal + fat_cal)
            carbs = round(carb_cal / 4)

            macros = {
                'calories': round(calories),
                'protein': protein,
                'carbs': carbs,
                'fat': fat
            }

            app.logger.info(f"Calculated macros for gender={gender}, goal={goal}, activity={activity}, body_fat={body_fat}")
        except Exception as e:
            app.logger.error(f"Macro calculation failed: {e}")

    return render_template('calculator.html', macros=macros)

if __name__ == '__main__':
    app.run(debug=True)
