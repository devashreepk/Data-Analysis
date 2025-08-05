import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

folder_path = r"/Users/devashreepk/Documents/Data analytics/python/Data-Analysis/E-commerce Data Analysis"
#Merge 12 months of Sales data into a single csv file
files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]
for file in files:
    print(file)

#Blank Dataframe
all_data = pd.DataFrame()

for file in files:
    current_df = pd.read_csv(folder_path +"/" + file)
    all_data = pd.concat([all_data, current_df])

#all_data.shape
print(all_data.shape)
#Convert into dataset
all_data.to_csv( r"/Users/devashreepk/Documents/Data analytics/python/Data-Analysis/E-commerce Data Analysis/all_data.csv",index=False)

#Data Cleaning and Formatting
print(all_data.dtypes)
print(all_data.head())

print(all_data.isnull().sum())


all_data = all_data.dropna(how ='all')
print(all_data.shape)

#Best month for Sale?
'05/20/20'.split('/')[0]

def month(x):
    return x.split('/')[0]

#Add month column

all_data['Month'] = all_data['Order Date'].apply(month)
print(all_data.dtypes)

all_data['Month'] = all_data['Month'].astype(str)
print(all_data['Month'].unique())

filter =all_data['Month'] == 'Order Date'
print(len(all_data[filter]))
print(all_data.shape)
print(all_data.head())

#remove header rows that may have been appended as data rows
all_data = all_data[all_data['Price Each'] != 'Price Each']

all_data['Price Each'] = all_data['Price Each'].astype(float)
all_data['Quantity Ordered'] = all_data['Quantity Ordered'].astype(int)
all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']

print(all_data.head())

#Sales total per month
print(all_data.groupby("Month") ["Sales"].sum())

#Graphs for sale as per month
months = range(1,13)
plt.bar(months, all_data.groupby("Month") ["Sales"].sum())
plt.xticks(months)
plt.ylabel("Sales")
plt.xlabel("Month Number")
plt.show()

#Which city has maximum orders?

def city(x):
    return x.split(',')[1]

all_data['city'] = all_data['Purchase Address'].apply(city)
print(all_data.groupby('city')['city'].count())

plt.bar(all_data.groupby('city')['city'].count().index, all_data.groupby('city')['city'].count())
plt.xticks(rotation = 'vertical')
plt.ylabel("Received orders")
plt.xlabel("City Names")
plt.show()

#What time should we display advertisements to maximise product purchase?
all_data['Order Date'][0].dtype

all_data = all_data[all_data['Order Date'] != 'Order Date']  # remove header rows
all_data = all_data.dropna(subset=['Order Date'])

all_data['Order Date'] = pd.to_datetime(all_data['Order Date'], format='%m/%d/%y %H:%M')

all_data['Hour'] = all_data['Order Date'].dt.hour
hours = all_data['Hour'].value_counts().sort_index()

plt.figure(figsize = (10,6))
plt.plot(hours.index, hours.values)
plt.title("Orders by Hour of Day")
plt.xlabel("Hour of Day")
plt.ylabel("Number of Orders")
plt.grid()
plt.xticks(range(0,24))
plt.show()



#keys = []
#hour = []
#for key,hour_df in all_data.groupby('Hour'):
 #   keys.append(key)
  #  hour.append(len(hour_df))

#plt.grid()
#plt.plot(keys,hour)

# What are the Best selling products and why?
product_group = all_data.groupby('Product')['Quantity Ordered'].sum()
product_group.plot(kind = 'bar', figsize = (12,6))
plt.title("Best selling Product")
plt.xlabel("Product")
plt.ylabel("Total Quantity Ordered")
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()

print(all_data.groupby('Product')['Price Each'].mean())

products = all_data.groupby('Product')['Quantity Ordered'].sum().index
quantity = all_data.groupby('Product')['Quantity Ordered'].sum()
prices = all_data.groupby('Product')['Price Each'].mean()

plt.figure(figsize=(40,24))
fig,ax1 = plt.subplots()
ax2=ax1.twinx()
ax1.bar(products, quantity, color='g')
ax2.plot(products, prices, 'b-')
ax1.set_xticklabels(products, rotation='vertical', size=8)
plt.show()
print(all_data.shape)

#what products are most often sold together?
#Orders that have same order id are sold mostly together

df = all_data[all_data['Order ID'].duplicated(keep = False)]
print(df.head(20))

df['Grouped'] = df.groupby('Order ID') ['Product'].transform(lambda x: ','.join(x))
print(df.head())
print(all_data.shape)

#Drop out all duplicate order ID
df2 = df.drop_duplicates(subset =['Order ID'])

df2['Grouped'].value_counts() [0:5].plot.pie()
plt.show()

import plotly.graph_objs as go
from plotly.offline import iplot
values=df2['Grouped'].value_counts()[0:5]
labels=df['Grouped'].value_counts()[0:5].index

trace=go.Pie(labels=labels, values=values,
               hoverinfo='label+percent', textinfo='value',
               textfont=dict(size=25),
              pull=[0, 0, 0,0.2, 0]
               )
iplot([trace])
plt.show()
