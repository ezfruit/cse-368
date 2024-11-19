function refresh() {
    const chatMessages = document.getElementById("chat-messages");
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function sendMessage() {
    const user_input = document.getElementById("user-input");
    const user_message = user_input.value.trim();
    if (!user_message) return; // Do nothing for empty input
    user_input.value = "";

    const messageJson = { "message": user_message };
    fetch("/message_sent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(messageJson)
    })
    .then(response => response.json())
    .then(data => {
        updateChatBox(data);
        refresh();
    });
}

function updateChatBox(data) {
    const chatMessages = document.querySelector(".chat-messages");
    data.forEach(item => {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", item.name === "user" ? "user" : "bot");
        messageDiv.innerHTML = `${item.name}: ${item.message}`;
        chatMessages.appendChild(messageDiv);
    });
}
