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
            food_ids = request.form.getlist('food_id')
            quantities = request.form.getlist('quantity')

            # Ensure parallel food_id and quantity pairs
            if len(food_ids) != len(quantities):
                raise ValueError("Mismatched food_id and quantity inputs")

            # Create or retrieve recipe
            recipe = conn.execute("SELECT id FROM recipes WHERE name = ?", (recipe_name,)).fetchone()
            if not recipe:
                conn.execute("INSERT INTO recipes (name) VALUES (?)", (recipe_name,))
                conn.commit()
                current_app.logger.info(f"Created new recipe: {recipe_name}")
                recipe_id = conn.execute("SELECT id FROM recipes WHERE name = ?", (recipe_name,)).fetchone()['id']
            else:
                current_app.logger.warning(f"Attempted to create a duplicate recipe: {recipe_name}")
                return redirect('/recipes')

            # Add all ingredients
            for food_id_str, qty_str in zip(food_ids, quantities):
                food_id = int(food_id_str)
                quantity = float(qty_str)
                conn.execute("""
                    INSERT INTO recipe_items (recipe_id, food_id, quantity)
                    VALUES (?, ?, ?)""",
                    (recipe_id, food_id, quantity)
                )
                current_app.logger.info(f"Added ingredient (Food ID: {food_id}, Quantity: {quantity}) to recipe ID {recipe_id}")

            conn.commit()
            current_app.logger.info(f"Successfully saved recipe: {recipe_name} (ID: {recipe_id})")

        except Exception as e:
            current_app.logger.error(f"Error updating recipe: {e}")

        return redirect('/recipes')

    # GET: Display form and recipes
    foods = conn.execute("SELECT * FROM foods").fetchall()
    recipe_rows = conn.execute("SELECT * FROM recipes").fetchall()
    recipes = []

    for recipe in recipe_rows:
        ingridents = []
        items = conn.execute("""
            SELECT f.name, fi.quantity, f.calories, f.protein, f.carbs, f.fat, f.fiber
            FROM recipe_items fi
            JOIN foods f ON fi.food_id = f.id
            WHERE fi.recipe_id = ?""", (recipe['id'],)).fetchall()

        for item in items:
            ingridents.append((item['name'], item['quantity']))

        total_cals = sum(item['calories'] * item['quantity'] / 100 for item in items)
        total_prot = sum(item['protein'] * item['quantity'] / 100 for item in items)
        total_carb = sum(item['carbs'] * item['quantity'] / 100 for item in items)
        total_fat = sum(item['fat'] * item['quantity'] / 100 for item in items)
        total_fiber = sum(item['fiber'] * item['quantity'] / 100 for item in items)

        recipes.append({
            'id': recipe['id'],
            'name': recipe['name'],
            'ingredients': ingridents,
            'calories': round(total_cals, 1),
            'protein': round(total_prot, 1),
            'carbs': round(total_carb, 1),
            'fat': round(total_fat, 1),
            'fiber': round(total_fiber, 1)
        })

    current_app.logger.info("Displayed recipe list")
    return render_template('recipes.html', foods=foods, recipes=recipes)

@recipes_bp.route('/delete/<int:recipe_id>', methods=["POST"])
def delete_recipe(recipe_id):
    try:
        conn = get_db()
        
        # First delete associated items
        conn.execute("DELETE FROM recipe_items WHERE recipe_id = ?", (recipe_id,))
        
        # Then delete the recipe itself
        conn.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        
        conn.commit()
        current_app.logger.info(f"Deleted recipe ID {recipe_id} and its items")
    except Exception as e:
        current_app.logger.error(f"Error deleting recipe ID {recipe_id}: {e}")
    return redirect('/recipes')

