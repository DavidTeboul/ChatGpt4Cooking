import os
import gspread
import pandas as pd
import openai
from oauth2client.service_account import ServiceAccountCredentials
from openai import ChatCompletion


def export_to_sheet():
    # Connect to Google Sheets
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('gs_credentials.json', scope)
    client = gspread.authorize(credentials)
    print(credentials)
    # Open the spreadsheet
    sheet = client.open('GPT4Cooking_data').sheet1
    # Get all values from the worksheet
    values = sheet.get_all_values()
    # Create a DataFrame from the values
    df = pd.DataFrame(values[1:], columns=values[0])
    column_quantite = 'Quantite'  # Specify the name of the column you want to delete
    label = df.drop(column_quantite, axis=1)
    # Delete rows with the specific value in the last column
    label_clean_1 = label[label.iloc[:, -1] != '1']
    label_clean_1_2 = label_clean_1[label_clean_1.iloc[:, -1] != '2']
    products = label_clean_1_2.iloc[:, 0]
    print(products)
    return products


def chat_with_assistant():
    openai.organization = "org-1Wig5szKzDYWI9tUmk1nfBES"
    openai.api_key = "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"

    conversation = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

    while True:
        user_input = input('')
        conversation.append({'role': 'user', 'content': user_input})

        response = ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=conversation,
            temperature=2,
            max_tokens=250,
            top_p=0.9
        )

        assistant_response = response['choices'][0]['message']['content']
        conversation.append({'role': 'assistant', 'content': assistant_response})
        print('\n' + assistant_response + '\n')

if __name__ == '__main__':
    myProducts = export_to_sheet()
    print("My products : ",myProducts.values)
    chat_with_assistant()
