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
});
