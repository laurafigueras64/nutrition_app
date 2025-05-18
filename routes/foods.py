from flask import Blueprint, render_template, request, redirect, current_app
from db import get_db
from utils import get_number_or_zero
import logging

foods_bp = Blueprint('foods', __name__, url_prefix='/foods')

@foods_bp.route('/', methods=['GET', 'POST'])
def foods():
    conn = get_db()
    if request.method == 'POST':
        try:
            name = request.form['name']
            calories = get_number_or_zero(request.form.get('calories'))
            protein = get_number_or_zero(request.form.get('protein'))
            carbs = get_number_or_zero(request.form.get('carbs'))
            fat = get_number_or_zero(request.form.get('fat'))
            fiber = get_number_or_zero(request.form.get('fiber'))
            conn.execute("""
                INSERT INTO foods (name, calories, protein, carbs, fat, fiber)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (name, calories, protein, carbs, fat, fiber)
            )
            conn.commit()
            current_app.logger.info(f"Added food: {name}")
        except Exception as e:
            current_app.logger.error(f"Error adding food: {e}")
        return redirect('/foods')
    
    foods = conn.execute("SELECT * FROM foods").fetchall()
    current_app.logger.info("Displayed food list")
    return render_template('foods.html', foods=foods)

@foods_bp.route('/delete/<int:food_id>', methods=['POST'])
def delete_food(food_id):
    try:
        conn = get_db()
        conn.execute("DELETE FROM foods WHERE id = ?", (food_id,))
        conn.commit()
        current_app.logger.info(f"Deleted food ID {food_id}")
    except Exception as e:
        current_app.logger.error(f"Error deleting food ID {food_id}: {e}")
    return redirect('/foods')

@foods_bp.route('/edit/<int:food_id>', methods=['GET', 'POST'])
def edit_food(food_id):
    conn = get_db()
    if request.method == 'POST':
        try:
            name = request.form['name']
            calories = get_number_or_zero(request.form.get('calories'))
            protein = get_number_or_zero(request.form.get('protein'))
            carbs = get_number_or_zero(request.form.get('carbs'))
            fat = get_number_or_zero(request.form.get('fat'))
            fiber = get_number_or_zero(request.form.get('fiber'))
            conn.execute("""
                UPDATE foods
                SET name = ?, calories = ?, protein = ?, carbs = ?, fat = ?, fiber = ?
                WHERE id = ?
            """, (name, calories, protein, carbs, fat, fiber, food_id))
            conn.commit()
            current_app.logger.info(f"Updated food ID {food_id}")
            return redirect('/foods')
        except Exception as e:
            current_app.logger.error(f"Error updating food: {e}")
    food = conn.execute("SELECT * FROM foods WHERE id = ?", (food_id,)).fetchone()
    return render_template('edit_food.html', food=food)

