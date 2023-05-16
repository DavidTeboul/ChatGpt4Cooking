import numpy as np
import pandas as pd
import gspread
import openai
import time
from oauth2client.service_account import ServiceAccountCredentials
from openai import ChatCompletion
from base64 import b64decode


def myProducts_to_sheet():
    # Connect to Google Sheets
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('gs_credentials.json', scope)
    client = gspread.authorize(credentials)
    # print(credentials)
    # Open the spreadsheet
    sheet_product = client.open('GPT4Cooking_data').sheet1
    sheet_recite = client.open('GPT4Cooking_data').get_worksheet(1)
    # Get all values from the worksheet
    values_product = sheet_product.get_all_values()
    values_recite = [row[1:] for row in sheet_recite.get_all_values()[1:] if any(row[1:])]
    # Create a DataFrame from the values
    df_product = pd.DataFrame(values_product[1:], columns=values_product[0])
    df_recite = pd.DataFrame(values_recite[1:], columns=values_recite[0])
    column_quantity = 'Quantite'  # Specify the name of the column you want to delete
    label = df_product.drop(column_quantity, axis=1)
    # Delete rows with the specific value in the last column
    label_clean_1 = label[label.iloc[:, -1] != '1']
    label_clean_1_2 = label_clean_1[label_clean_1.iloc[:, -1] != '2']
    label_clean_1_2_3 = label_clean_1_2[label_clean_1_2.iloc[:, -1] != '3']
    label_clean_1_2_3_4 = label_clean_1_2_3[label_clean_1_2_3.iloc[:, -1] != '4']
    products = label_clean_1_2_3_4.iloc[:, 0]
    print("\n Import WorkSheet Done ! \n ")
    return products


def myPlanning_to_sheet():
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('gs_credentials.json', scope)
    client = gspread.authorize(credentials)
    # Open the spreadsheet
    sheet_recite = client.open('GPT4Cooking_data').get_worksheet(1)
    # Get all values from the worksheet
    values_recite = [row[1:] for row in sheet_recite.get_all_values()[1:] if any(row[1:])]
    # Create a DataFrame from the values
    df_recite = pd.DataFrame(values_recite[1:], columns=values_recite[0])
    column_array = df_recite.iloc[:, 1].values
    column_array_new = pd.Series(column_array)
    return column_array_new


def chat_with_assistant_question(question):
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


def chat_with_assistant_input():
    openai.organization = "org-1Wig5szKzDYWI9tUmk1nfBES"
    openai.api_key = "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"

    conversation = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

    while True:
        user_input = input("You: ")
        conversation.append({'role': 'user', 'content': user_input})

        response = ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=conversation,
            temperature=2,
            max_tokens=250,
            top_p=0.9
        )

        assistant_response = response.choices[0].message.content
        conversation.append({'role': 'assistant', 'content': assistant_response})

        print("Assistant:", assistant_response)
        time.sleep(10)


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
        with open(f'{prefix}_{i}_{prompt}.jpg', 'wb') as file:
            file.write(b64decode(image))
    time.sleep(10)


def GPT4_GenerateImage_Cooking(responses_Image):
    print('\n')
    print('\n')
    print("Attendez, je génère un aperçu .....")
    print('\n')
    for j in range(2, len(responses_Image) - 1):
        print(responses_Image[j], "......")
        GPT4_GenerateImage((responses_Image[j]), 1, j)
    exit(0)


def GPT4_Proposition(my_products, response):
    question_Before_List = "J'ai juste besoin de quelques idées de repas à faire avec la liste que je t'ai donnée. (sans me donner d'explications sur la preparation)"
    questionArray = [
        "Salut",
        "Pouvez-vous me donner 5 repas sains que je peux me faire pour ce soir suivant une liste de produits que j'ai ?",
        str(my_products.values),
        question_Before_List,
        "Super ! Merci beaucoup !"
    ]
    for i in range(len(questionArray)):
        if questionArray[i] == question_Before_List:
            array_elements = chat_with_assistant_question(questionArray[i]).split("\n")
            response = array_elements
        else:
            chat_with_assistant_question(questionArray[i])
    return response


def GPT4_Planning(my_planning, response):
    question_Before_List = "J'ai juste besoin de quelques idées de repas à faire avec la liste que je t'ai donnée. (sans me donner d'explications sur la preparation)"
    questionArray = [
        "Salut",
        "Peux tu me reproposer un planning de plats part semaine en te basant sur une liste de repas que je te donne ? ",
        "Peux tu me generer en te basant sur une liste de repas ? ",
        str(my_planning.values),
        "Si tu Peux me reproposer un planning de plats pour la semaine avec ?",
        "Super ! Merci beaucoup !"
    ]
    for i in range(len(questionArray)):
        chat_with_assistant_question(questionArray[i])
    return response


if __name__ == '__main__':
    responses_products = np.array([])
    responses_planning = np.array([])
    while True:
        # Display the menu options
        print("Menu:\n")
        print("1. Export to sheet\n")
        print("2. Process with GPT4 Proposition Cooking\n")
        print("3. Process with GPT4 Planning Cooking\n")
        print("4. Generate Image with GPT4 Cooking\n")
        print("5. Generate chat \n")
        print("6. Exit\n")
        choice = input("Enter your choice (1-5): \n")
        if choice == '1':
            myProducts = myProducts_to_sheet()
            myPlanning = myPlanning_to_sheet()
            print("\n Data exported to sheet successfully. \n")
        elif choice == '2':
            responses_products = GPT4_Proposition(myProducts, responses_products)
            print("\nGPT4 Proposition processing completed.\n")
        elif choice == '3':
            responses_planning = GPT4_Planning(myPlanning, responses_planning)
            print("\nGPT4 Planning processing completed.\n")
        elif choice == '4':
            GPT4_GenerateImage_Cooking(responses_products)
            print("\nImage generation with GPT4 Cooking completed.\n")
        elif choice == '5':
            chat_with_assistant_input()
            print("\nGenerate chat completed.\n")
        elif choice == '6':
            print("\nExiting the program...\n")
            break
        else:
            print("Invalid choice. Please try again.")

# responses = GPT4Cooking(myProducts, responses)
# GPT4_GenerateImage_Cooking(responses)
