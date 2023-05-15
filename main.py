import os
import gspread
import pandas as pd
import openai
from oauth2client.service_account import ServiceAccountCredentials
from openai import ChatCompletion
import time


def export_to_sheet():
    # Connect to Google Sheets
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('gs_credentials.json', scope)
    client = gspread.authorize(credentials)
    # print(credentials)
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
    label_clean_1_2_3 = label_clean_1_2[label_clean_1_2.iloc[:, -1] != '3']
    label_clean_1_2_3_4 = label_clean_1_2_3[label_clean_1_2_3.iloc[:, -1] != '4']
    products = label_clean_1_2_3_4.iloc[:, 0]
    # print(products)
    return products


def chat_with_assistant(question):
    openai.organization = "org-1Wig5szKzDYWI9tUmk1nfBES"
    openai.api_key = "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"
    conversation = [{'role': 'system', 'content': 'You are a helpful assistant.'}]
    print('\n' + question + '\n')
    conversation.append({'role': 'user', 'content': question})
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
    time.sleep(5)


def GPT4Cooking(myProducts):
    questionArray = [
        "hi",
        "can you help me to know what I can eat healthy tonight?",
        "Can I give you a list of ingredients I have for helping you?",
        str(myProducts.values),
        "I just need some propositions for healthy lunch"
        "can you try again to propose me please ?",
    ]
    for i in range(len(questionArray)):
        chat_with_assistant(questionArray[i])


if __name__ == '__main__':
    myProducts = export_to_sheet()
    GPT4Cooking(myProducts)
