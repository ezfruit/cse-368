
function refresh() {
    return 0;
}
function sendMessage() {
    const user_input = document.getElementById("user-input");
    const user_message = user_input.value;
    user_input.value = "";
    const messageJson = {"message": user_message}

    const response = fetch("/message_sent", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        }, 
        body: JSON.stringify(messageJson)
    })
    .then(response => response.json())
    .then(data => {
        updateChatBox(data);
    });
}

function updateChatBox(data) {
    const chatMessages = document.querySelector(".chat-messages");

    if (data.length > 0) {
        for (let object = 0; object < data.length; object++) {
            let user = data[object]["name"];
            let message = data[object]["message"];

            // If the message contains a URL, convert it to a clickable link
            message = convertUrlsToLinks(message);

            if (user === "user") {
                if (message.length === 0) {
                    break;
                }
                const userMessages = document.createElement("div");
                userMessages.classList.add('message', 'user');
                userMessages.innerHTML = `${user}: ${message}`;
                chatMessages.appendChild(userMessages);
            }
            else {
                const botMessages = document.createElement("div");
                botMessages.classList.add('message', 'bot');
                botMessages.innerHTML = `${user}: ${message}`;
                chatMessages.appendChild(botMessages);
            }
        }
    }
}

// Function to detect URLs and convert them to clickable links
function convertUrlsToLinks(text) {
    const urlPattern = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlPattern, (url) => {
        return `<a href="${url}" target="_blank">${url}</a>`;
    });
}
