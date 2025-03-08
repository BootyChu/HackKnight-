function updateSlider(sliderId, displayId) {
    const slider = document.getElementById(sliderId);
    const display = document.getElementById(displayId);

    // Define label mappings for each slider
    const incomeLabels = ["Below $30k", "$30k-$50k", "$50k-$70k", "$70k-$90k", "$90k-$100k", "$100k+"];
    const creditLabels = ["Poor", "Fair", "Good", "Very Good", "Excellent"];

    // Choose the correct label based on slider ID
    if (sliderId === "income-range") {
        display.textContent = incomeLabels[slider.value];
    } else if (sliderId === "credit-score") {
        display.textContent = creditLabels[slider.value];
    }
}


document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form"); // Select the form
    const progressBar = document.getElementById("progress-fill"); // Progress bar fill
    const sections = document.querySelectorAll(".form-group"); // Sections of the form
    const inputs = form.querySelectorAll("input, select, textarea"); // All form elements

    function updateProgress() {
        let completedSections = 0;
        let totalSections = sections.length;

        sections.forEach(section => {
            let inputsInSection = section.querySelectorAll("input, select, textarea");
            let sectionCompleted = false;

            inputsInSection.forEach(input => {
                if (input.type === "checkbox" || input.type === "radio") {
                    if (input.checked) sectionCompleted = true;
                } else if (input.type === "range" || input.value.trim() !== "") {
                    sectionCompleted = true;
                }
            });

            if (sectionCompleted) completedSections++;
        });

        // Calculate progress percentage based on sections filled
        let progress = (completedSections / totalSections) * 100;
        progressBar.style.width = progress + "%"; // Update width of progress bar

        // If form is fully completed, make sure the bar is exactly 100%
        if (completedSections === totalSections) {
            progressBar.style.width = "100%";
        }
    }

    // Listen for user input and update progress bar
    inputs.forEach(input => {
        input.addEventListener("input", updateProgress);
    });

    // Call function once on page load to check pre-filled values
    updateProgress();
});


// login page
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("signup-tab")?.addEventListener("click", function () {
        // Redirect to the register page when "Sign Up" tab is clicked
        window.location.href = "/register";
    });

    document.getElementById("login-tab")?.addEventListener("click", function () {
        // Redirect to the login page when "Log In" tab is clicked
        window.location.href = "/login";
    });
});





// Tab switching (for visual effect)
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('login-tab')?.addEventListener('click', function() {
        document.getElementById('login-tab').classList.add('active');
        document.getElementById('signup-tab').classList.remove('active');
        document.getElementById('login-form').classList.add('active');
        document.getElementById('signup-form').classList.remove('active');
    });

    document.getElementById('signup-tab')?.addEventListener('click', function() {
        document.getElementById('signup-tab').classList.add('active');
        document.getElementById('login-tab').classList.remove('active');
        document.getElementById('signup-form').classList.add('active');
        document.getElementById('login-form').classList.remove('active');
    });
});

document.addEventListener("DOMContentLoaded", function () {
    fetch("static/data/cards.csv")
        .then(response => response.text())
        .then(csvText => {
            const cardsArray = parseCSV(csvText);
            renderCards(cardsArray);
        })
        .catch(error => console.error("Error loading CSV file:", error));

    function parseCSV(csvText) {
        csvText = csvText.replace(/\r\n/g, "\n").trim();
        const lines = csvText.split("\n");
        const headers = lines[0].split(",").map(h => h.trim());

        return lines.slice(1).map(line => {
            let values = [];
            let current = "";
            let insideQuotes = false;

            for (let char of line) {
                if (char === '"' && !insideQuotes) {
                    insideQuotes = true;
                } else if (char === '"' && insideQuotes) {
                    insideQuotes = false;
                } else if (char === "," && !insideQuotes) {
                    values.push(current.trim());
                    current = "";
                } else {
                    current += char;
                }
            }
            values.push(current.trim());

            if (values.length !== headers.length) {
                return null;
            }

            return headers.reduce((acc, header, index) => {
                acc[header.replace(/\s+/g, " ").trim()] = values[index] || "N/A";
                return acc;
            }, {});
        }).filter(card => card !== null);
    }

    function renderCards(cards) {
        const container = document.getElementById("card-container");
        if (!container) return;

        container.innerHTML = "";

        if (cards.length === 0) {
            container.innerHTML = "<p>No cards available.</p>";
            return;
        }

        cards.forEach(card => {
            const cardHTML = `
                <div class="card-recommendation">
                    <div class="card-image">${card["Card Name"] || "Unknown Card"}</div>
                    <div class="card-content">
                        <span class="card-tag">${card["Credit Level"] || "N/A"}</span>
                        <h3 class="card-title">${card["Card Name"] || "Unknown"}</h3>
                        <div class="card-features">
                            <div class="feature-item"><span class="feature-icon-small">✓</span> ${card["Reward"] || "No rewards info"}</div>
                            <div class="feature-item"><span class="feature-icon-small">✓</span> Annual Fee: ${card["Annual Fee"] || "Not specified"}</div>
                            <div class="feature-item"><span class="feature-icon-small">✓</span> Purchase Rate: ${card["Purchase Rate"] || "N/A"}</div>
                            <div class="feature-item"><span class="feature-icon-small">✓</span> Transfer Info: ${card["Transfer Info"] || "N/A"}</div>
                        </div>
                    </div>
                </div>
            `;
            container.innerHTML += cardHTML;
        });
    }
});
