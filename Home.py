import streamlit as st
import pandas as pd
from skimage import io, color, util, transform
from Backend import knn_predict, glcm_matrix

st.set_page_config(page_title="IEIS", page_icon="😎")
st.title("Welcome to IEIS! 👋")
st.caption("Image Emotion Identification System (IEIS) is a web-based application that can analyze the sentiment of an image. This app utilizes the GLCM method for texture analysis and the K-Nearest Neighbors (KNN) algorithm for sentiment classification.")

uploaded_file = st.file_uploader("Choose a file", type=['png', 'jpg', 'jpeg'])
k = st.number_input("Enter the value of k", min_value=1)

if uploaded_file is None:
    st.button("Predict", disabled=True)
else:
    if st.button("Predict"):
        image = io.imread(uploaded_file)

        if image.shape[0] > 48 or image.shape[1] > 48:
            image = transform.resize(image, (48, 48))

        if len(image.shape) == 3:  # Check if the image has color channels
            image = color.rgb2gray(image)

        image = util.img_as_ubyte(image)
        new_features = glcm_matrix(image)
        prediction, accuracy_percentage = knn_predict(new_features, k)

        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption=uploaded_file.name, use_column_width=True)

        with col2:
            sentiment = "Happy 😊" if prediction == 1 else "Sad 😔"
            data_df = pd.DataFrame({"sentiment": [sentiment], "accuracy": [accuracy_percentage]})
            st.dataframe(data_df)
