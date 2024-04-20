import streamlit as st
import langchain_helper as lch
import google_form_helper as gf
from dotenv import dotenv_values

# Load environment variables from .env file
env_vars = dotenv_values('.env')

# Access the DRIVE_FOLDER_ID variable
drive_folder_id = env_vars['DRIVE_FOLDER_ID']

# set title
st.title("Market Research Survey Generator")

# define drop down list
user_goal = st.sidebar.selectbox("What is your goal?", ("Measure Marketing Effectiveness", "Assess Market Demand", "Evaluate Competitor Landscape", "Optimize Pricing Strategies", "Enhance Brand Perception"))

# define text block
user_industry = st.sidebar.text_area(
    label='Industry',
    max_chars=25,
    help= '',
    placeholder = 'Car Manufacturing',
    value = 'Car Manufacturing'
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
    if user_industry and user_product:
        print('User Submitted')
        # generate statements based on user options
        response = lch.generate_survey_statements(user_goal, user_industry, user_product)
        print('Survey Statements Generated!')
        # extract text 
        response_text = response['text']
        st.success('Survey Statements Generated!')
        st.markdown(response_text)
        # create google form on Drive
        if generate_form_checkbox:
            print('User Requested Google Form')
            # form name
            form_name = user_goal +  ' of ' + user_product
            # generate form
            results = gf.google_form_generator(raw_text=response_text, folder_id= drive_folder_id, form_name=form_name, form_description='Please respond on a scale 1-5')
            print('User Form Created!')
            st.success('Google Form Uploaded to Drive!')
        else:
            st.stop()
    else:
        st.warning("Please provide values for both industry and product.")
