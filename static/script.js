document.addEventListener("DOMContentLoaded", () => {
    // Auto-focus the first input field on each form
    const firstInput = document.querySelector("form input, form select, form textarea");
    if (firstInput) {
        firstInput.focus();
    }

    // Simple numeric validation: Replace empty numeric fields with 0 before submission
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", () => {
            const inputs = form.querySelectorAll("input[type='number']");
            inputs.forEach(input => {
                if (input.value.trim() === "") {
                    input.value = 0;
                }
            });
        });
    });

    // Highlight the current nav link
    const navLinks = document.querySelectorAll("nav a");
    const path = window.location.pathname;
    navLinks.forEach(link => {
        if (link.getAttribute("href") === path) {
            link.classList.add("active");
        }
    });

    const recipeCards = document.querySelectorAll(".recipe-card");
    recipeCards.forEach(card => {
        try {
            const rawData = card.dataset.recipe;

            const validJson = rawData
                .replace(/'/g, '"')
                .replace(/\((.*?)\)/g, '[$1]');


            const recipeData = JSON.parse(validJson);

            addRecipeCard(card, recipeData);
        } catch (error) {
            console.error("Error parsing recipe data:", error);
        }
    });
});

function addIngredient() {
    const container = document.getElementById('ingredients-container');
    const newIngredient = document.createElement('div');
    newIngredient.classList.add('ingredient');
    newIngredient.innerHTML = `
        <select name="food_id">
            ${foodsOptionsHTML}
        </select>
        <input name="quantity" type="number" step="0.1" placeholder="Quantity (g)">
    `;
    container.appendChild(newIngredient);
}

function addRecipeCard(card, recipe) {
    if (card.innerHTML) {
        card.innerHTML = '';
    }
    const recipeList = document.getElementById('recipe-list');

    const name = document.createElement('h3');
    name.textContent = recipe.name;
    card.appendChild(name);

    const content = document.createElement('div');
    content.className = 'recipe-content';
    card.appendChild(content);

    const ingredientsList = document.createElement('ul');
    recipe.ingredients.forEach(ingredient => {
        const item = document.createElement('li');
        item.textContent = `${ingredient[1]}g ${ingredient[0]}`;
        ingredientsList.appendChild(item);
    });
    content.appendChild(ingredientsList);

    const graphCanvas = document.createElement('canvas');
    graphCanvas.id = `graph-${recipe.id}`;
    content.appendChild(graphCanvas);

    recipeList.appendChild(card);

    new Chart(graphCanvas, {
        type: 'pie',
        data: {
            labels: ['Protein', 'Carbs', 'Fat', 'Fiber'],
            datasets: [{
                data: [recipe.protein, recipe.carbs, recipe.fat, recipe.fiber],
                backgroundColor: ['#4caf50', '#2196f3', '#ff9800', '#f44336'],
            }]
        },
        options: {
            responsive: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom'
                }
            }
        }
    });
}