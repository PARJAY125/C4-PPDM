import streamlit as st
import re
import os
import pandas as pd
from Backend import knn_score, get_data

st.set_page_config(page_title="C4 PPDM - Machine", page_icon="😎")
st.title("Machine ⚙️")

txt = st.text_area('Enter k values separated by commas', placeholder='3, 5, 7, 9')
valid_characters = "0123456789, \n"

def case_folding(sentence):
    sentence = re.sub(r'\s+', ' ', sentence)
    return sentence

def display_accuracy_testing():
    st.subheader('Percentage of Accuracy Testing')
    k_values = [int(k.strip()) for k in txt.split(',') if k.strip().isdigit()]
    accuracy = [knn_score(n) for n in k_values]
    chart_data = pd.DataFrame(
        {'k': [float(val) for val in accuracy]},
        index=k_values
    )
    st.area_chart(chart_data)

def display_data_info():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Data Percentage')
        positive_images = os.listdir("dataset/happy/")
        negative_images = os.listdir("dataset/sad/")
        chart_data = pd.DataFrame(
            {
                'happy': [len(positive_images)],
                'sad': [len(negative_images)]
            },
            index=['sentiment']
        )
        st.bar_chart(chart_data)
    with col2:
        st.subheader('Data Info')
        train_data, test_data = get_data()
        data_df1 = pd.DataFrame({"train": [train_data]})
        data_df2 = pd.DataFrame({"test": [test_data]})
        st.dataframe(data_df1)
        st.dataframe(data_df2)

if txt == '':
    submit = st.button('Submit', disabled=True)
    display_accuracy_testing()
    display_data_info()
else:
    submit = st.button('Submit', disabled=False)
    if submit:
        display_accuracy_testing()
        display_data_info()
