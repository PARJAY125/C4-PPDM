import streamlit as st
import os
import math

st.set_page_config(page_title="C4 PPDM - Dataset", page_icon="😎")
st.title("Dataset 📂")

image_folder_happy = "dataset training/happy/"
image_folder_sad = "dataset training/sad/"

type = st.radio("Select type", ('All', 'Happy', 'Sad'), index=0, key='type')

if type == 'All':
    happy_image_files = [os.path.join(image_folder_happy, img) for img in os.listdir(image_folder_happy)]
    sad_image_files = [os.path.join(image_folder_sad, img) for img in os.listdir(image_folder_sad)]
    image_files = happy_image_files + sad_image_files
    file_names = [os.path.basename(file) for file in happy_image_files] + [os.path.basename(file) for file in sad_image_files]
elif type == 'Happy':
    image_files = [os.path.join(image_folder_happy, img) for img in os.listdir(image_folder_happy)]
    file_names = os.listdir(image_folder_happy)
else:
    image_files = [os.path.join(image_folder_sad, img) for img in os.listdir(image_folder_sad)]
    file_names = os.listdir(image_folder_sad)

row = st.number_input("Enter the value of row", min_value=1, max_value=math.ceil(len(image_files) / 6))

columns = st.columns(6)
for i in range(row):
    for j in range(6):
        index = i * 6 + j
        if index < len(image_files):
            with columns[j]:
                st.image(image_files[index], caption=file_names[index])
