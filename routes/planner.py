from flask import Blueprint, render_template, request, redirect, current_app
from db import get_db
from utils import get_number_or_zero
import logging

planner_bp = Blueprint('planner', __name__, url_prefix='/planner')

@planner_bp.route('/', methods=['GET', 'POST'])
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
            current_app.logger.info(f"Planned meal '{meal}' on {date} using recipe ID {recipe_id}")
        except Exception as e:
            current_app.logger.error(f"Error adding meal plan: {e}")
        return redirect('/planner')

    recipes = conn.execute("SELECT * FROM recipes").fetchall()
    plans = conn.execute("""
        SELECT mp.date, mp.meal, r.name AS recipe_name
        FROM meal_plans mp
        JOIN recipes r ON mp.recipe_id = r.id
        ORDER BY mp.date
    """).fetchall()
    current_app.logger.info("Displayed meal planner")
    return render_template('planner.html', recipes=recipes, plans=plans)