import streamlit as st

from emotion_model import emotion_predict
from datetime import datetime
import logging

name = st.text_input("Please enter your sentence here:")
result = ""
result_check = ""
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

if (st.button('Submit')):
    result = name.title()
    try:
        result_check = emotion_predict(result)
    except Exception as E:
        result_check = "Error"
        print(E)
    st.success(result_check)

user_response = st.text_input("Please give your emotion that you are thinking is correct")
if (st.button('Submit Feedback')):
    if user_response:
        st.info("Thank you for contributing")
        logging.info(f"{result}, {result_check},  {user_response}, {datetime.now()}")
    else:
        st.info("Thank you for using")
        logging.info(f"{result}, {result_check}, {datetime.now()}")
