# Data-Visualization
Author: Meredith Winslow (mwinslow2@elon.edu)
Purpose: This repository is for the course project of MGT 4250 at [Elon University](https://www.elon.edu/)

## Project Description
Link to Visualization Application:
This repository seeks insight about customer churn within the telecommunications industry. The specific questions I want to answer with my visualizations are:
- Q1: Which types of contracts result in the highest customer churn?
- Q2: Does age have an impact on whether a customer will churn?
- Q3: For customers who did churn, what were the main reasons for doing so? Do the reasons vary by gender?
  
## Importance Statement
These questions are  **important** because they can help telecommunications companies focus money on retaining current customers who are at risk for churning.

## Data Description
I was able to download the data directly from Kaggle into an excel, which I cleaned to include only the following columns: Customer ID, Gender (male or female), Contract (month-by-month, one-year, or two-year), Customer Status (joined, churned, or stayed) and Churn Category(competitor, dissatisfaction, price, attitude, or other). All of the variables are categorical. The link to my data set is here:   https://www.kaggle.com/datasets/shilongzhuang/telecom-customer-churn-by-maven-analytics

## Interpreting Visualizations
Here is a link to my streamlit application: [https://meredithvisualizationfinal.streamlit.app/](https://meredithvisualizationfinal.streamlit.app/)

<img width="407" alt="image" src="https://github.com/mer-winslow/Data-Visualization/assets/168783522/adc8fafd-9673-4fe0-b730-4820cc3d4ffb">

This visualization answers my question about which contracts result in the highest customer churn- month-to-month contracts. By using a bar chart to display each respective churn percentage it makes it clear which category is highest.

<img width="304" alt="image" src="https://github.com/mer-winslow/Data-Visualization/assets/168783522/7766474b-a16d-494e-88be-c928d8ea4104">

This question answers my question about whether age has an effect on the likelihood that a customer will churn. As seen in the bar graph, older customers had higher percent churn than younger customers. 

<img width="323" alt="image" src="https://github.com/mer-winslow/Data-Visualization/assets/168783522/0b88c94e-7992-43c0-92f5-00e1a04f8418">

For this visualization I decided to use a tree map to break down the top reasons for customer churn by gender. This answers my question, showing that the most common reason for churn among men and women was a competitor and the second most common reason for churn was attitude for women and dissatisfaction for men.

## Discussion & Summary
**Related Article**
https://www.clientsuccess.com/resources/true-cost-customer-churn-part-1#:~:text=Not%20only%20does%20churn%20mean,to%20retain%20your%20current%20ones.
The link above belongs to an article called the "True Cost of Churn". My inital questions sought insight to the types of customers that are more likely to churn, and the most common reasons for doing so. The importance of these insights are highlighted in the article, which states that the cost of aquiring new customers is 5x that of retaining current ones. If telecommunications companies can focus their efforts on high risk groups such as older customers (figure 2) and better advertize longer contracts (figure 3), they can reduce churn levels and reduce the cost of needing to find new customers.

**ChatGPT Attempt**
I asked ChatGPT my initial questions to see if it would produce conclusions similar to the ones reached with my visualisations. This is the answer it gave:
-Q1: Month-to-month contracts typically result in the highest customer churn in the telecommunications industry due to their flexibility allowing customers to leave without penalties.
-Q2: Yes, age can have a significant impact on customer churn in the telecommunications industry. Younger customers, often more tech-savvy and seeking the best deals and latest features, tend to switch providers more frequently. Older customers may prefer stability and consistency, leading to lower churn rates.
-Q3: Customers often churn due to factors like high prices, poor service quality, unsatisfactory customer support, unfavorable contract terms, or outdated technology, with the reasons sometimes varying by gender based on different preferences and usage patterns.
AI seemed to do well with question 1 and 3, but I was suprised to see that it gave an answer opposite to my findings for question 2. My visualization shows that older aged customers are more likely to churn, not younger. 

##Code

```
import pandas as pd
import streamlit as st
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
```
