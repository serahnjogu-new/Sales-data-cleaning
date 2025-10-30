# Import the necessary libraries
import pandas as pd
import numpy as np

# load the data set 
df = pd.read_csv(r"C:\Users\Serah\Downloads\sales_data_week1_500rows.csv")
print (df.head())
# Data set shape
print("Shape of dataset:", df.shape)

#Check for missing values
print(df.isnull().sum())

# Drop all rows where Name and Product are 
df = df.dropna(subset=['Name', 'Product'])

# Fill missing 'Region' with 'Unknown'
df['Region'] = df['Region'].fillna('Unknown')

# Fill missing 'Purchase_Amount' with mean
df['Purchase_Amount'] = df['Purchase_Amount'].fillna(df['Purchase_Amount'].mean())

#convert purchase date column to date time format
df['Purchase Date'] = pd.to_datetime(df['Purchase Date'], errors='coerce')

# New column from purchase date
df['Purchase_Year'] = df['Purchase Date'].dt.year

# Rename all columns to lowercase and replace spaces with underscores
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Rename purchase_amount to amount_usd
df = df.rename(columns={'purchase_amount': 'amount_usd'})

# Filter and sort data in descending order
filtered_df = df[df['amount_usd'] > 1000].sort_values(by='amount_usd', ascending=False)
print(filtered_df.head())
# Data aggregation
agg = df.groupby('region').agg(
    total_purchases=('amount_usd', 'count'),
    average_purchase_amount=('amount_usd', 'mean')
)
print(agg)

# create a new column called category
def categorize(amount):
    if amount >= 1000:
        return "High"
    elif amount >= 500:
        return "Medium"
    else:
        return "Low"

df['category'] = df['amount_usd'].apply(categorize)
df.head()
# Export as csv
df.to_csv('cleaned_sales_data.csv', index=False)






