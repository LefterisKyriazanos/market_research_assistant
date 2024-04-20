from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
import os

import random

def get_credentials() -> Credentials:
    # Define the scopes for Google Forms API
    scopes = ['https://www.googleapis.com/auth/forms', 
              'https://www.googleapis.com/auth/drive']
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Define raw text input
raw_text = """
Question 1: What is your favorite color?
Question 2: How would you rate our product? (1 - Poor, 2 - Fair, 3 - Good, 4 - Excellent)
"""

def copy_file(file_id: str, destination_folder_id: str, new_name='') -> str:
    
    creds = get_credentials()
    file_metadata = {
        'parents': [destination_folder_id],
        'name': new_name
    }
    if new_name:
        file_metadata['name'] = new_name
    
    service = build('drive', 'v3', credentials=creds)
    file = service.files().copy(fileId=file_id,
                                body=file_metadata,
                                fields='id',
                                supportsAllDrives=True, 
                            ).execute()
    
    return file.get('id')

def delete_file(file_id:str):
    retry_count = 0 
    time_sleep = 30
    while retry_count <= 3:
        try:
            creds = get_credentials()
            service = build('drive', 'v3', credentials=creds)
            service.files().delete(fileId=file_id, supportsAllDrives=True).execute()
            return 0
        except Exception as err:
            print(err)
            print(f'retries: {retry_count}')
            if retry_count == 3:
                print('Operation failed way too many times')
                print('Program will terminate. Try again later..')
                raise Exception from err
            print("Operation Failed..")
            print(f"Retrying in {time_sleep} seconds (max retries = 3)")
            time.sleep(time_sleep)
            time_sleep = time_sleep * 2
            retry_count += 1

def relocate_file(file_id, target_folder_id, new_file_name):
    new_file_id = copy_file(file_id, target_folder_id, new_file_name)
    delete_file(file_id)
    return new_file_id

def add_question(client, question, question_index, formId):
     
    new_question  = {
        "requests": [
            {
                "createItem": {
                 "item": {
                "title": question,
                "questionItem": {
                    "question": {
                        "required": True,
                        "choiceQuestion": {
                            "type": "RADIO",
                            "options": [
                                {"value": "1"},
                                {"value": "2"},
                                {"value": "3"},
                                {"value": "4"},
                                {"value": "5"}
                            ]
                        }
                    }
                }
                    },
                    "location": {"index": question_index},
                }
            }
        ]
    }

     # Update the form with a question
    question_setting = (
        client.forms()
        .batchUpdate(formId=formId, body=new_question)
        .execute()
    )
        
def add_form_description(client, form_id, description):
    # Request body to add description to a Form
    update = {
        "requests": [
            {
                "updateFormInfo": {
                    "info": {
                        "description": (
                           description
                        ),
                    },
                    "updateMask": "description",
                }
            }
        ]
    }
    # Update the form with a description
    update_description = (
        client.forms()
        .batchUpdate(formId=form_id, body=update)
        .execute()
    )


def google_form_generator(raw_text, folder_id, form_name, form_description):
    # Authenticate and create a service
    creds = get_credentials()
    forms_service = build('forms', 'v1', credentials=creds)
    # Split raw text into individual questions
    questions = raw_text.strip().split('\n')

    # Create a new Google Form
    createResult = forms_service.forms().create(
        body={
        "info": {
        "title": form_name,
        # 'description': 'This is a survey form created from raw text.', 
        # 'folderId': folder_id
    }}
    ).execute()
    form_id = createResult["formId"]

    # returns new file id of relocated file
    form_id = relocate_file(form_id, target_folder_id=folder_id, new_file_name= form_name)
    # add description
    add_form_description(forms_service, form_id, form_description)
 
    # add questions/statements
    for index, question in enumerate(questions):
        print(question)
        add_question(client=forms_service, question=question, formId=form_id, question_index = index)

     # Print the result to see it now has a video
    result = forms_service.forms().get(formId=form_id).execute()
    print(result)
    print("Survey Form created successfully.")

if __name__ == "__main__":
    # print(generate_survey_statements("car manufacturing", "electric cars"))
    # Generate a random number between 1 and 1000
    random_number = random.randint(1, 1000)
    form_name = f'{random_number}_latest_form'
    print(form_name)
    # google_form_generator(raw_text, '1ghOnW9RKaINHnUz3aPqMBPHlyW2FCkn-', form_name=form_name)
    # print('ok')
