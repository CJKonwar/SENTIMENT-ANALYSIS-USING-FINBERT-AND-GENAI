<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
    <title>Chatbot</title>
</head>
<body>
    <div id="chat">
        <h1>Chatbot</h1>
        <div id="messages"></div>
        <input type="text" id="userMessage" placeholder="Type your message here">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        async function sendMessage() {
            const message = document.getElementById('userMessage').value;
            const response = await fetch('/chatbot/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': '{{ csrf_token() }}',
                },
                body: JSON.stringify({ message }),
            });
            const data = await response.json();
            document.getElementById('messages').innerHTML += `<p>You: ${message}</p><p>Bot: ${data.reply}</p>`;
        }
    </script>
</body>
</html>
