import streamlit as st
import langchain_helper as lch
import google_form_helper as gf

st.title("Market Research Survey Generator")

user_goal = st.sidebar.selectbox("What is your goal?", ("Measure Marketing Effectiveness", "Assess Market Demand", "Evaluate Competitor Landscape", "Optimize Pricing Strategies", "Enhance Brand Perception"))

user_industry = st.sidebar.text_area(
    label='Industry',
    max_chars=25,
    help= '',
    placeholder = 'Car Manufacturing',
    value = 'Car Manufacturing'
)

user_product = st.sidebar.text_area(
    label='Product',
    max_chars= 50,
    help= 'a short description of your product and features',
    placeholder = 'Ford Mustang Mach‑E® electric SUV',
    value = 'Ford Mustang Mach‑E® electric SUV'
)



submit_button = st.sidebar.button('Submit')
generate_form_checkbox = st.sidebar.checkbox('Generate Google Form in Google Drive')
generate_form_button = False
response_text =  ''
if submit_button:
    if user_industry and user_product:
        print('User Submitted')
        response = lch.generate_survey_statements(user_goal, user_industry, user_product)
        print('Survey Statements Generated!')
        response_text = response['text']
        st.success('Survey Statements Generated!')
        st.markdown(response_text)
        # st.text('Click to generate Google Form in Google Drive')
        # generate_form_button = st.button('Generate Google Form')
        if generate_form_checkbox:
            print('User Requested Google Form')
            form_name = user_goal +  ' of ' + user_product
            gf.google_form_generator(response_text, '1ghOnW9RKaINHnUz3aPqMBPHlyW2FCkn-', form_name, 'Please respond on a scale 1-5')
            print('User Form Created!')
            st.success('Google Form Uploaded to Drive!')
        else:
            st.stop()
    else:
        st.warning("Please provide values for both industry and product.")
