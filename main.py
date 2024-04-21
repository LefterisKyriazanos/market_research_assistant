import streamlit as st
import langchain_helper as lch
import google_form_helper as gf
import translator_helper as lang_helper
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values('.env')
language_codes = lang_helper.language_codes

# Access the DRIVE_FOLDER_ID variable
drive_folder_id = env_vars['DRIVE_FOLDER_ID']

# set title
st.title("Market Research Survey Generator")

# Get list of language names
language_names = sorted(set(list(language_codes.keys())))

# Create select box for selecting languages in the sidebar
user_language = st.sidebar.selectbox("Language", language_names)

# Get the language code corresponding to the selected language
user_language_code = language_codes[user_language]

# define drop down list
user_goal = st.sidebar.selectbox("I want to", ( "Assess Market Demand", "Measure Marketing Effectiveness", "Evaluate Competitor Landscape", "Enhance Brand Perception", "Optimize Pricing Strategies"))

# define text block
user_industry = st.sidebar.text_area(
    label='Industry',
    max_chars=25,
    help= '',
    placeholder = 'Automotive',
    value = 'Automotive'
)

# define text block
user_product = st.sidebar.text_area(
    label='Product',
    max_chars= 50,
    help= 'a short description of your product and features',
    placeholder = 'Ford Mustang Mach‑E® electric SUV',
    value = 'Ford Mustang Mach‑E® electric SUV'
)


# define submit button
submit_button = st.sidebar.button('Submit')
# checkbox to generate Google Form
generate_form_checkbox = st.sidebar.checkbox('Generate Google Form in Google Drive')

response_text =  ''
if submit_button:
    if user_industry and user_product and user_language:
        print('User Submitted')
        # generate statements based on user options
        response = lch.generate_survey_statements(user_goal, user_industry, user_product)
         # extract text to list
        response_text = response['text'].strip().split('\n')
        print('Survey Statements Generated!')
        st.success('Survey Statements Generated (English)!')
        if user_language_code != 'en_XX':
            # processing message
            with st.spinner(f'Translating in {user_language}...'):
                print(f'Translating Statements to {user_language}..')
                # translate..
                response_text = lang_helper.translate_survey_questions(text_list=response_text, target_lng=user_language_code)
                text = '\n'.join(response_text)
                
            st.success(f'Survey Statements Translated to {user_language}!')
            st.markdown(text)
        else:
            st.markdown(response['text'])
            
        # create google form on Drive
        if generate_form_checkbox:
            print('User Requested Google Form')
            print('Generating Form..')
            with st.spinner('Generating Form..'):
                # form name
                form_name = f'({user_language})' + ' ' + user_goal +  ' of ' + user_product
                # generate form
                results = gf.google_form_generator(text_list=response_text, folder_id=drive_folder_id, form_name=form_name, form_description= 'Please respond on a scale 1-5')
                print('User Form Created!')
                st.success('Google Form Uploaded to Drive!')
        else:
            st.stop()
    else:
        st.warning("Please provide values for language, industry and product.")
