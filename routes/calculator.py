from flask import Blueprint, render_template, request, redirect, current_app
from db import get_db
from utils import get_number_or_zero
import logging

calculator_bp = Blueprint('calculator', __name__, url_prefix='/calculator')

@calculator_bp.route('/', methods=['GET', 'POST'])
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

            current_app.logger.info(f"Calculated macros for gender={gender}, goal={goal}, activity={activity}, body_fat={body_fat}")
        except Exception as e:
            current_app.logger.error(f"Macro calculation failed: {e}")

    return render_template('calculator.html', macros=macros)