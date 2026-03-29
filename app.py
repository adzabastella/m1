import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.title("File uploader")
st.subheader("Input csv")
uploaded_files=st.file_uploader("choose a file")

if uploaded_files:
    df=pd.read_csv(uploaded_files)
    st.subheader('Dataframe')
    st.write(df)
    col1, col2= st.columns(2)
    with col1:
        fig1=plt.figure()
        sns.scatterplot(x='EstimatedSalary', y='Age', hue='Purchased', data=df)
        st.pyplot(fig1)
    with col2:
        fig2=plt.figure()
        sns.histplot('df.Age')
        st.pyplot(fig2)