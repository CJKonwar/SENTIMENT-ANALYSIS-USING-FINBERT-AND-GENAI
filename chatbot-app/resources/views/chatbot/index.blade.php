<!-- resources/views/chatbot.blade.php -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chatbot</title>
    <style>
        /* Dark Theme Styling */
        body {
            background-color: #1e1e2f;
            color: #e0e0e0;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }

        #chat {
            background-color: #2a2a3c;
            border-radius: 8px;
            padding: 20px;
            width: 300px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
        }

        h1 {
            text-align: center;
            color: #ffffff;
            font-size: 1.5em;
        }

        #messages {
            background-color: #33334a;
            border-radius: 8px;
            padding: 10px;
            height: 200px;
            overflow-y: auto;
            margin-bottom: 10px;
            color: #cfcfcf;
        }

        #messages p {
            margin: 0;
            padding: 5px;
            border-radius: 4px;
        }

        #messages p:nth-child(odd) {
            background-color: #3b3b4f;
        }

        #messages p:nth-child(even) {
            background-color: #4b4b64;
        }

        input[type="text"] {
            width: calc(100% - 22px);
            padding: 10px;
            margin-top: 10px;
            margin-bottom: 10px;
            border: 1px solid #444455;
            border-radius: 5px;
            background-color: #2a2a3c;
            color: #ffffff;
        }

        button {
            width: 100%;
            padding: 10px;
            background-color: #5a5ad1;
            border: none;
            border-radius: 5px;
            color: #ffffff;
            cursor: pointer;
            font-size: 1em;
        }

        button:hover {
            background-color: #4a4ac1;
        }
    </style>
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



