import streamlit as st
import langchain_helper as lch

st.title(":clipboard: Market Research Assistant")

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

if submit_button:
    if user_industry and user_product:
        response = lch.generate_survey_statements(user_goal, user_industry, user_product)
        st.text(response['text'])
    # st.stop()
# animal_type = st.sidebar.selectbox("What is your pet?", ("Dog", "Cat", "Hamster", "Rat", "Snake", "Lizard", "Cow"))
