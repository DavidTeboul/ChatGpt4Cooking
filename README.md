# GPT4Cooking Chatbot

GPT4Cooking Chatbot is a Python script that utilizes the OpenAI API and Google Sheets API to create a chatbot using the GPT-3.5 Turbo model. The chatbot engages in a conversation with the user, providing suggestions for healthy meals based on the available ingredients.

## Prerequisites

Before running this script, make sure you have the following prerequisites:

- Python 3.x installed
- Required Python libraries: gspread, pandas, openai, oauth2client
  You can install these dependencies by running the following command:

### pip install gspread pandas openai oauth2client


## Configuration

To use the GPT4Cooking chatbot, you need to configure the script with your API credentials and Google Sheets credentials. Follow these steps:

1. Open `gs_credentials.json` and replace it with your Google Sheets API credentials file, which you can obtain by creating a service account in the Google Cloud Console.

2. Sign up for an account on the OpenAI website and obtain your API key from the OpenAI dashboard.

3. Open the Python script in a text editor.




## Usage

1. Make sure the gs_credentials.json file is in the same directory as the Python script.

2. Open a terminal and navigate to the directory where the script is located.
3. Run the script using the following command:
### python <script_name>.py

- The chatbot will prompt you with a series of questions and suggestions based on your inputs and the available ingredients stored in the Google Sheets.

- Follow the conversation prompts in the terminal and observe the chatbot's responses.

- The conversation continues until the script finishes running or you terminate it manually.

## Customization
 
- You can modify the behavior of the chatbot by adjusting the parameters in the chat_with_assistant() function. For example, you can change the temperature, max_tokens, or top_p values to influence the response generation.

- Please note that the script provided is a basic example, and you can extend it or modify it to suit your specific requirements. You can integrate additional functionality or improve the chatbot's capabilities as needed.

## Google Sheets Integration

- The script connects to Google Sheets to retrieve available ingredients. To use this feature, make sure you have set up the Google Sheets API and have the necessary credentials in the gs_credentials.json file. The script assumes the Google Sheets file is named "GPT4Cooking_data" and the ingredients are stored in the first sheet.

 ```python
 
This project is designed to help with cooking-related tasks. It uses different libraries and tools to perform various functions:

Connecting to Google Sheets: The project connects to Google Sheets to access and retrieve data from specific worksheets.

Data Manipulation: The retrieved data is organized and cleaned using a library called pandas. This helps to prepare the data for further analysis.

Chatting with the Assistant: The project uses a powerful language model called GPT-3.5 Turbo to engage in conversations. Users can ask questions or provide prompts, and the model responds with helpful information.

Image Generation: The project can generate image previews based on certain prompts. These images can provide visual representations of the cooking ideas or concepts discussed.

Meal Suggestions: By providing a list of available ingredients or products, the project can suggest meal ideas for users. This can help with meal planning and deciding what to cook.

Meal Planning: Users can input a list of meals they want to include in their weekly plan, and the project can provide a meal schedule based on that input.

The project presents a user-friendly menu with different options, allowing users to export data to Google Sheets, receive meal suggestions and plans, generate image previews, engage in chat conversations, or exit the program.

Overall, this project aims to make cooking tasks easier by leveraging technology and intelligent algorithms to provide assistance and ideas.
