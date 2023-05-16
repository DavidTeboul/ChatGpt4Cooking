import os
import gspread
import numpy as np
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
    time.sleep(10)
    return assistant_response


def GPT4_GenerateImage(prompt, image_count, i):
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
        with open(f'{prefix}_{i}.jpg', 'wb') as file:
            file.write(b64decode(image))
    time.sleep(5)


def GPT4_GenerateImage_Cooking(responses_Image):
    print(responses_Image)
    print("GPT4_GenerateImage_Cooking")
    for j in range(2, len(responses_Image) - 1):
        print(responses_Image[j])
        GPT4_GenerateImage((responses_Image[j]), 1, j)


def GPT4Cooking(my_products, response):
    questionArray = [
        "Salut",
        "Pouvez-vous me donner 5 repas sains que je peux me faire pour ce soir suivant une liste de produits que j'ai ?",
        str(my_products.values),
        "J'ai juste besoin de quelques idées de repas à faire avec la liste que je t'ai donnée. (sans me donner d'explications sur la preparation)",
        "Super ! Merci beaucoup !"
    ]
    for i in range(len(questionArray)):
        if questionArray[
            i] == "J'ai juste besoin de quelques idées de repas à faire avec la liste que je t'ai donnée. (sans me donner d'explications sur la preparation)":
            print(1)
            array_elements = chat_with_assistant(questionArray[i]).split("\n")
            response = array_elements
        else:
            chat_with_assistant(questionArray[i])
    return response


if __name__ == '__main__':
    responses = np.array([])
    myProducts = export_to_sheet()
    responses = GPT4Cooking(myProducts, responses)
    GPT4_GenerateImage_Cooking(responses)
# d='Salade de poulet grillé avec des légumes verts mélangés, des noix, des fruits frais et une vinaigrette légère.'
# c = ' Poisson grillé avec légumes vapeur : '
# GPT4_GenerateImage(c, image_count=5)
