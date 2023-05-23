from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
from openai import ChatCompletion

app = Flask(__name__)

load_dotenv()
openai.organization = os.getenv("OPENAI_API_ORGANISATION")
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chat Assistant</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/css/bootstrap.min.css">
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 20px;
            }

            #conversation {
                height: 300px;
                overflow-y: scroll;
                border: 1px solid #ccc;
                padding: 10px;
            }

            #user-input {
                width: 70%;
                padding: 5px;
                font-size: 16px;
            }

            #send-button {
                padding: 5px 10px;
                font-size: 16px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="text-center">Chat Assistant</h1>
            <div id="conversation" class="mb-3"></div>
            <div class="input-group mb-3">
                <input type="text" id="user-input" class="form-control" placeholder="Type your message...">
                <button id="send-button" class="btn btn-primary" onclick="sendMessage()">Send</button>
            </div>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
        <script>
            function sendMessage() {
                var userInput = document.getElementById("user-input").value;
                appendMessage("You: " + userInput);

                axios.post('/assistant', {
                    user_input: userInput
                })
                .then(function(response) {
                    var assistantResponse = response.data.assistant_response;
                    appendMessage("Assistant: " + assistantResponse);
                })
                .catch(function(error) {
                    console.log(error);
                });

                document.getElementById("user-input").value = "";
            }

            function appendMessage(message) {
                var conversationDiv = document.getElementById("conversation");
                conversationDiv.innerHTML += "<p>" + message + "</p>";
                conversationDiv.scrollTop = conversationDiv.scrollHeight;
            }
        </script>
    </body>
    </html>
    '''


@app.route('/assistant', methods=['POST'])
def assistant():
    user_input = request.json['user_input']
    conversation = [{'role': 'system', 'content': 'You are a professional chef , with kosher restriction .'},
                    {'role': 'user', 'content': user_input}]
    response = ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversation,
        temperature=0.1,
        max_tokens=250,
        top_p=0.9
    )
    assistant_response = response.choices[0].message.content
    conversation.append({'role': 'assistant', 'content': assistant_response})

    print("Assistant:", assistant_response)

    return jsonify({'assistant_response': assistant_response})


if __name__ == '__main__':
    app.run()
