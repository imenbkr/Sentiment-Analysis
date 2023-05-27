/* app.js */
document.addEventListener('DOMContentLoaded', function() {
    const reviewForm = document.getElementById('review-form');
    const chatForm = document.getElementById('chat-form');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const recommendationsList = document.getElementById('recommendations-list');

    reviewForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const reviewInput = document.getElementById('review').value;

        // Send the review to the server and receive the prediction
        fetch('/review', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ Reviews: reviewInput })
        })
        .then(response => response.json())
        .then(data => {
            // Update the chatMessages div with the prediction
            appendMessage('You', reviewInput);
            appendMessage('Prediction', data.prediction);
        })
        .catch(error => {
            console.error('Error:', error);
        });

        document.getElementById('review').value = '';
    });

    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const userMessage = userInput.value;
        appendMessage('You', userMessage);

        // Send user message to the server and receive chatbot's response
        fetch('/recommendation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_input: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Update the chatMessages div with the chatbot's response
            appendMessage('Chatbot', data.response);
        })
        .catch(error => {
            console.error('Error:', error);
        });

        userInput.value = '';
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement('p');
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatMessages.appendChild(messageElement);
    }

    // Function to add recommended products to the recommendations list
    function addRecommendation(product) {
        const li = document.createElement('li');
        li.textContent = product;
        recommendationsList.appendChild(li);
    }

    // Example code to fetch product recommendations from the server
    fetch('/get_recommendations')
        .then(response => response.json())
        .then(data => {
            // Update the recommendations list with the received recommendations
            data.recommendations.forEach(product => {
                addRecommendation(product);
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
