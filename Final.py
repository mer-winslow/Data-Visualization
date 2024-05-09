import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv("telecom_customer_churn.csv")

#1
churned_customers = df[df['Customer Status'] == 'Churned']

churn_by_contract = churned_customers['Contract'].value_counts().reset_index()
churn_by_contract.columns = ['Contract Type', 'Number of Churned Customers']

fig1 = px.bar(churn_by_contract, 
             x='Contract Type', 
             y='Number of Churned Customers',
             title='Number of Churned Customers by Contract Type',
             color='Contract Type',  
             labels={'Contract Type': 'Contract Type', 'Number of Churned Customers': 'Number of Churned Customers'},
             template='plotly_white')

#2
bins = [18, 30, 40, 50, 60, 70, 80, 90, 100]
df['Age Group'] = pd.cut(df['Age'], bins=bins, right=False)

df['Age Group'] = df['Age Group'].astype(str)

age_group_churn = df.groupby('Age Group')['Customer Status'].apply(lambda x: (x == 'Churned').mean() * 100).reset_index()
age_group_churn.columns = ['Age Group', 'Percentage of Churned Customers']

fig2 = px.bar(age_group_churn, 
            x='Age Group', 
            y='Percentage of Churned Customers',
            title='Percentage of Churned Customers by Age Group',
            labels={'Age Group': 'Age Group', 'Percentage of Churned Customers': 'Percentage (%)'},
            color='Age Group', 
            template='plotly_white')
#3
churned_customers = df[df['Customer Status'] == 'Churned']
churn_reasons_gender = churned_customers[churned_customers['Churn Reason'].notna()]

counts = churn_reasons_gender.groupby(['Gender', 'Churn Reason']).size().reset_index(name='Counts')

fig3 = px.treemap(counts, 
                 path=['Gender', 'Churn Reason'], 
                 values='Counts',
                 color='Gender',
                 color_discrete_map={'Male': 'blue', 'Female': 'red'},
                 title='Tree Map of Churn Reasons by Gender')



col1, col2, col3 = st.columns([0.4, 0.3, 0.3])

with col1:
    st.plotly_chart(fig1, use_container_width=True)
with col2:
    st.plotly_chart(fig2, use_container_width=True)
with col3:
    st.plotly_chart(fig3, use_container_width=True)