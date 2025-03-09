document.getElementById("chat-form").addEventListener("submit", function(event) {
    event.preventDefault();
    const userMessage = document.getElementById("user-input").value;
    document.getElementById("user-input").value = "";

    fetch("/help_support", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        const chatBox = document.getElementById("chat-response");

        // Display AI response in chat
        if (data.error) {
            chatBox.innerHTML += `<p style="color: red;"><strong>Error:</strong> ${data.error}</p>`;
            return;
        }

        chatBox.innerHTML += `<p><strong>Bot:</strong> Here are the top 3 credit cards for you:</p>`;

        // Display the top 3 recommended cards
        displayRecommendedCards(data.cards);
    })
    .catch(error => console.error("Error:", error));
});

// Function to generate HTML for recommended credit cards
function createCardHTML(card) {
    return `
        <div class="card-recommendation">
            <div class="card-content">
                <h3 class="card-title">${card.card_name}</h3>
                <span class="card-tag">${card.credit_level}</span>
                <div class="card-features">
                    <p><strong>Rewards:</strong> ${card.reward}</p>
                    <p><strong>Annual Fee:</strong> ${card.annual_fee}</p>
                    <p><strong>Purchase Rate:</strong> ${card.purchase_rate}</p>
                    <p><strong>Transfer Info:</strong> ${card.transfer_info}</p>
                </div>
                <a href="#" class="btn btn-accent">Apply Now</a>
            </div>
        </div>`;
}

// Function to display the top 3 recommended cards
function displayRecommendedCards(cards) {
    const cardContainer = document.getElementById("card-container");
    cardContainer.innerHTML = "";  // Clear previous content

    if (cards.length === 0) {
        cardContainer.innerHTML = "<p>No recommendations available.</p>";
        return;
    }

    cards.forEach(card => {
        cardContainer.innerHTML += createCardHTML(card);
    });
}