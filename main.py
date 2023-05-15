import os
import gspread
import pandas as pd
import openai
from oauth2client.service_account import ServiceAccountCredentials
from openai import ChatCompletion
import time
import webbrowser
from base64 import b64decode


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
    return assistant_response


def GPT4_GenerateImage(prompt, image_count):
    openai.organization = "org-1Wig5szKzDYWI9tUmk1nfBES"
    openai.api_key = "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"
    images = []
    response = openai.Image.create(
        prompt=prompt,
        n=image_count,
        size='512x512',
        response_format='b64_json',
    )
    for image in response['data']:
        images.append(image.b64_json)
    prefix = 'Img'
    for index, image in enumerate(images):
        with open(f'{prefix}_{index}.jpg', 'wb') as file:
            file.write(b64decode(image))


def GPT4Cooking(myProducts):
    questionArray = [
        "Salut",
        "Pouvez-vous m'aider à savoir quoi manger de sain ce soir ?",
        "Est-ce que je peux vous donner une liste d'ingrédients que j'ai pour vous aider ?",
        str(myProducts.values),
        "au moin 5 propositions de repas sains que je pourrais préparer avec cette liste.",
        "Pouvez-vous me donner des explications sur la façon de la propsition avec le saummon?",
        "Quel repas est le plus simple et rapide à préparer parmi ces propositions ?",
        "Plus d'explications si possible",
        "Super ! Merci beaucoup !"
    ]
    for i in range(len(questionArray)):
        chat_with_assistant(questionArray[i])


#   for i in range(len(questionArray)):
#     if questionArray[i]== 'au moin 5 propositions de repas sains que je pourrais préparer avec cette liste.':
#         chat_with_assistant(questionArray[i])
#    else:
#       chat_with_assistant(questionArray[i])

if __name__ == '__main__':
    # myProducts = export_to_sheet()
    # GPT4Cooking(myProducts)
    # GPT4_GenerateImage('smoke montain', image_count=1)
    # d='Salade de poulet grillé avec des légumes verts mélangés, des noix, des fruits frais et une vinaigrette légère.'
    c = ' Poisson grillé avec légumes vapeur : '
    GPT4_GenerateImage(c, image_count=5)
