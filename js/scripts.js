/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
// Show the "Go to Top" button when the user scrolls down
window.addEventListener('scroll', function() {
  const scrollToTopButton = document.querySelector('.go-to-top');
  if (window.pageYOffset > 300) {
    scrollToTopButton.classList.add('show');
  } else {
    scrollToTopButton.classList.remove('show');
  }
});

// JavaScript code for the chatbot functionality

// Function to toggle the chatbot container
function toggleChatbot() {
  var chatbotContainer = document.querySelector('.chatbot-container');
  chatbotContainer.style.transform = chatbotContainer.style.transform === 'translateX(-100%)' ? 'translateX(0)' : 'translateX(-100%)';
}

// Function to append user and chatbot messages to the chat window
function appendMessage(message, isUser = false) {
  var chatbotMessages = document.getElementById('chatbotMessages');
  var messageDiv = document.createElement('div');
  messageDiv.className = isUser ? 'user-message' : 'chatbot-message';
  messageDiv.textContent = message;
  chatbotMessages.appendChild(messageDiv);
}

// Function to handle user input and get the chatbot response
function sendMessage() {
  var userInput = document.getElementById('chatInput').value;
  if (userInput.trim() === '') {
    return;
  }
  appendMessage(userInput, true);
  document.getElementById('chatInput').value = '';

  // Call the ChatGPT API to get the chatbot response
  // Replace 'YOUR_API_KEY' with your actual API key
  var apiKey = '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';
  var apiUrl = 'https://api.openai.com/v1/engines/davinci-codex/completions';
  var headers = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`
  };

  var data = {
    'prompt': userInput,
    'max_tokens': 100
  };

  fetch(apiUrl, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {
    var chatbotResponse = result.choices[0].text.trim();
    appendMessage(chatbotResponse);
  })
  .catch(error => console.error('Error:', error));
}

// Event listener for chatbot close button
document.querySelector('.chatbot-close-btn').addEventListener('click', toggleChatbot);

// Show the chatbot container by default
toggleChatbot();
