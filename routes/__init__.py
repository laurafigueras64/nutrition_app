# routes/__init__.py
from .foods import foods_bp
from .recipes import recipes_bp
from .planner import planner_bp
from .calculator import calculator_bp

def register_routes(app):
    app.register_blueprint(foods_bp)
    app.register_blueprint(recipes_bp)
    app.register_blueprint(planner_bp)
    app.register_blueprint(calculator_bp)