CREATE TABLE foods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    calories REAL,
    protein REAL,
    carbs REAL,
    fat REAL
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE recipe_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER,
    food_id INTEGER,
    quantity REAL,
    FOREIGN KEY(recipe_id) REFERENCES recipes(id),
    FOREIGN KEY(food_id) REFERENCES foods(id)
);

CREATE TABLE meal_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    meal TEXT,
    recipe_id INTEGER,
    FOREIGN KEY(recipe_id) REFERENCES recipes(id)
);
