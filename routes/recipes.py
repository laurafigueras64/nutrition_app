from flask import Blueprint, render_template, request, redirect, current_app
from db import get_db
from utils import get_number_or_zero
import logging

recipes_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@recipes_bp.route('/', methods=['GET', 'POST'])
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
                recipes_bp.logger.info(f"Created new recipe: {recipe_name}")
                recipe_id = conn.execute("SELECT id FROM recipes WHERE name = ?", (recipe_name,)).fetchone()['id']
            else:
                recipe_id = recipe['id']

            conn.execute("""
                INSERT INTO recipe_items (recipe_id, food_id, quantity)
                VALUES (?, ?, ?)""",
                (recipe_id, food_id, quantity)
            )
            conn.commit()
            current_app.logger.info(f"Added food ID {food_id} to recipe '{recipe_name}' (qty: {quantity}g)")
        except Exception as e:
            current_app.logger.error(f"Error updating recipe: {e}")
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

        recipes.recipes_bpend({
            'name': recipe['name'],
            'calories': round(total_cals, 1),
            'protein': round(total_prot, 1),
            'carbs': round(total_carb, 1),
            'fat': round(total_fat, 1)
        })

    current_app.logger.info("Displayed recipe list")
    return render_template('recipes.html', foods=foods, recipes=recipes)