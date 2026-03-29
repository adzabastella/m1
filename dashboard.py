import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


df= pd.read_csv('bank.csv')
st.set_page_config(page_title='Real Time Science Dashboard', page_icon='✅✅', layout='wide')

st.title("Real life \ data analisis")
# filtre sur le type de job
job_filter= st.selectbox("select a job", pd.unique(df["job"]))
# creer un endroit pour le filtre
df= df[df["job"]== job_filter]

# indicateurs
avg_age= np.mean(df["age"])
count_maried=int(df[(df["marital"]=='married')]['marital'].count())
balance = np.mean(df['balance'])

kpi1, kpi2, kpi3=st.columns(3)

kpi1.metric(label='Age ⏳', value = round(avg_age), delta=round(avg_age))
kpi2.metric(label='Maried count 💍', value = round(count_maried), delta=round(count_maried))
kpi3.metric(label='Blance $', value = f"${round(balance,2)}", delta=round(balance/count_maried))

# graphiques
col1, col2=st.columns(2)
with col1:
    st.markdown('## FIRST CHART')
    fig1=plt.figure()
    sns.barplot(data=df, y='age', x='marital', palette='mako')
    st.pyplot(fig1)
with col2:
    st.markdown('## SECOND CHART')
    fig2=plt.figure()
    sns.histplot(data=df, y='age')
    st.pyplot(fig2)

st.markdown("## DETAILED DATA VIEW")
st.dataframe(df)