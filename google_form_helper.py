from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import Resource
from googleapiclient.discovery import build
import os

import random

def get_credentials() -> Credentials:
    """
    Get Google OAuth2 credentials.

    Returns:
    - Credentials: The OAuth2 credentials.

    This function retrieves OAuth2 credentials for accessing Google APIs,
    specifically the Google Forms and Google Drive APIs. It checks if there
    is a 'token.json' file containing previously authorized user credentials.
    If not, it initiates the OAuth2 authentication flow using client secrets
    from the 'credentials.json' file and prompts the user to authorize access.

    Example:
    ```python
    creds = get_credentials()
    ```

    Raises:
    - FileNotFoundError: If the 'credentials.json' file is missing.
    - ValueError: If the OAuth2 authentication flow fails or the credentials are invalid.
    """
    
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

def copy_file(file_id: str, destination_folder_id: str, new_name: str = ''):
    """
    Copy a file to a destination folder in Google Drive and optionally rename it.

    Parameters:
    - file_id (str): The ID of the file to be copied.
    - destination_folder_id (str): The ID of the destination folder where the file will be copied.
    - new_name (str): The new name for the copied file (optional).

    Returns:
    - str: The ID of the newly copied file.

    This function copies the specified file to the destination folder in Google Drive
    and optionally renames it with the provided new name. The ID of the newly copied
    file is returned.

    Example:
    ```python
    new_file_id = copy_file(file_id="your_file_id_here",
                             destination_folder_id="your_destination_folder_id_here",
                             new_name="new_file_name_here")
    ```
    """
    
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
    """
    Delete a file from Google Drive.

    Parameters:
    - file_id (str): The ID of the file to be deleted.

    Returns:
    - None

    This function deletes the specified file from Google Drive using the Drive API.

    Example:
    ```python
    delete_file(file_id="your_file_id_here")
    ```
    """
   
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)
    service.files().delete(fileId=file_id, supportsAllDrives=True).execute()

    
          

def relocate_file(file_id: str, target_folder_id: str, new_file_name: str):
    """
    Relocate a file to a target folder in Google Drive and optionally rename it.

    Parameters:
    - file_id (str): The ID of the file to be relocated.
    - target_folder_id (str): The ID of the target folder where the file will be moved.
    - new_file_name (str): The new name for the file after relocation (optional).

    Returns:
    - str: The ID of the newly relocated file.

    This function copies the specified file to the target folder in Google Drive and optionally
    renames it with the provided new file name. After copying, the original file is deleted,
    and the ID of the newly relocated file is returned.

    Example:
    ```python
    new_file_id = relocate_file(file_id="your_file_id_here",
                                 target_folder_id="your_target_folder_id_here",
                                 new_file_name="new_file_name_here")
    ```
    """

    new_file_id = copy_file(file_id= file_id, destination_folder_id= target_folder_id, new_name= new_file_name)
    delete_file(file_id)
    return new_file_id


def add_question_to_form(client: Resource, question: str, question_index: int, formId: str) -> None:
    """
    Add a question to a Google Form.

    Parameters:
    - client (Resource): The Google Forms client obtained from `build('forms', 'v1', credentials=creds)`.
    - question (str): The text of the question to add.
    - question_index (int): The index at which to add the question in the form.
    - formId (str): The ID of the Google Form to which the question will be added.

    Returns:
    - None

    This function adds a new question to a Google Form specified by its ID. The question
    is added at the specified index in the form's list of questions. The question type is
    set to "RADIO" with options ranging from 1 to 5.

    Example:
    ```python
    forms_service = build('forms', 'v1', credentials=creds)
    add_question_to_form(client=forms_service,
                            question="How satisfied are you with our product?",
                            question_index=3,
                            formId="your_form_id_here")
    ```

    Raises:
    - TypeError: If the `client` parameter is not of type `Resource`.
    """

    # Validate the client parameter
    if not isinstance(client, Resource):
        raise TypeError("The client parameter must be of type googleapiclient.discovery.Resource.")

    # Construct the request body to add the question
    new_question = {
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

    # Update the form with the new question
    question_setting = (
        client.forms()
        .batchUpdate(formId=formId, body=new_question)
        .execute()
    )
        
def add_form_description(client: Resource, form_id: str, description: str):
    """
    Add a description to a Google Form.

    Parameters:
    - client (Resource): The Google Forms client obtained from `build('forms', 'v1', credentials=creds)`.
    - form_id (str): The ID of the Google Form to which the description will be added.
    - description (str): The description to add to the Google Form.

    Returns:
    - None

    This function adds a description to a Google Form specified by its ID. The description
    is provided as input and is added to the form using the Google Forms API.

    Example:
    ```python
    forms_service = build('forms', 'v1', credentials=creds)
    add_form_description(client=forms_service,
                         form_id="your_form_id_here",
                         description="This is a survey form for collecting feedback.")
    ```
    Raises:
    - TypeError: If the `client` parameter is not of type `Resource`.
    """

    # Validate the client parameter
    if not isinstance(client, Resource):
        raise TypeError("The client parameter must be of type googleapiclient.discovery.Resource.")
    
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


def google_form_generator(raw_text: str, folder_id: str, form_name: str, form_description: str):
    
    """
    Generate a Google Form based on raw text input.

    Parameters:
    - raw_text (str): The raw text containing individual questions/statements separated by newlines.
    - folder_id (str): The ID of the folder where the Google Form will be placed.
    - form_name (str): The name of the Google Form.
    - form_description (str): The description of the Google Form.

    Returns:
    - None

    This function generates a new Google Form based on the provided raw text. It splits
    the raw text into individual questions/statements and creates a new Google Form with
    the specified name and description. The form is then relocated to the target folder
    specified by its ID. Finally, each question/statement is added to the form.

    Example:
    ```python
    raw_text = "Question 1?\nQuestion 2?\nQuestion 3?"
    google_form_generator(raw_text=raw_text,
                          folder_id="your_folder_id_here",
                          form_name="Survey Form",
                          form_description="This is a survey form.")
    ```

    Raises:
    - TypeError: If any of the input arguments are of invalid types.
    - ValueError: If any of the input arguments are empty strings or None.
    - HttpError: If there is an issue creating the form, relocating it, or adding questions to it.
    """
    
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
    }}
    ).execute()
    
    # get form id
    form_id = createResult["formId"]

    # relocate to target folder
    form_id = relocate_file(form_id, target_folder_id=folder_id, new_file_name= form_name)
    # add description
    add_form_description(client= forms_service, form_id= form_id, description= form_description)
 
    # add questions/statements
    for index, question in enumerate(questions):
        # print(question)
        add_question_to_form(client=forms_service, question=question, formId=form_id, question_index = index)

     # Print the result to see it now has a video
    result = forms_service.forms().get(formId=form_id).execute()
    # print(result)
    print("Survey Form created successfully.")
    return result

if __name__ == "__main__":
    # Generate a random number between 1 and 1000
    # random_number = random.randint(1, 1000)
    # form_name = f'{random_number}_latest_form'
    # print(form_name)
    # call function
    # google_form_generator(raw_text, '1ghOnW9RKaINHnUz3aPqMBPHlyW2FCkn-', form_name=form_name)
    print('ok')
