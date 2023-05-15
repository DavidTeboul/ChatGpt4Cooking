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

4. Replace the placeholder values with your API key and organization ID in the following section of the code:

 openai.organization = "org-1Wig5szKzDYWI9tUmk1nfBES"
 openai.api_key = "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"


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