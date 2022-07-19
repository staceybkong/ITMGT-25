import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

with open('transaction-data-adhoc-analysis.json', 'r') as f:
    data = json.load(f)
    
unprocessed_list = pd.DataFrame(data)

one_line_item = (unprocessed_list.set_index(['address', 'birthdate', 'mail', 'name', 'sex', 'username', 'transaction_value', 'transaction_date'])
   .apply(lambda x: x.str.split(';').explode())
   .reset_index())

one_line_item.drop(columns = ['mail', 'name', 'username'], inplace = True)

one_line_item[['birth year','birth month', 'birth day']]=one_line_item.birthdate.str.split('/',expand=True)
one_line_item.drop(columns = ['birthdate'], inplace = True)

from datetime import date
today = date.today()
one_line_item['birthyear'] = one_line_item['birth year'].astype(int)
age = today.year - one_line_item['birthyear']
                                     
one_line_item['age'] = age

one_line_item.drop(columns = ['birthyear', 'birth year', 'birth month', 'birth day'], inplace = True)

one_line_item[['transaction year','transaction month', 'transaction day']] = one_line_item.transaction_date.str.split('/',expand=True)
one_line_item.drop(columns = ['transaction day'], inplace = True)

one_line_item[['item1', 'item2', 'quantity']] = one_line_item['transaction_items'].str.split(',', expand=True)
one_line_item['item'] = one_line_item['item1'].str.cat(one_line_item[['item2']], sep=',')
one_line_item.drop(columns = ['transaction_items', 'item1', 'item2'], inplace = True)

one_line_item['item'].unique()

one_line_item['quantity'] = one_line_item['quantity'].str.replace("x","")
one_line_item['quantity'] = one_line_item['quantity'].str.strip("()")

one_line_item['quantity'] = one_line_item['quantity'].astype(int)
pivot1 = one_line_item.pivot_table(index=['transaction year', 'transaction month','item'], values=['quantity'], aggfunc='sum')

pip install dataframe_image

import dataframe_image as dfi

dfi.export(pivot1,"PivotTable1.png")

one_line_item['item'].unique()

price_dict = {'Exotic Extras,Beef Chicharon': 1299,
              'HealthyKid 3+,Nutrional Milk': 1990,
              'Candy City,Orange Beans': 199,
              'HealthyKid 3+,Gummy Vitamins': 1500,
              'HealthyKid 3+,Yummy Vegetables': 500,
              'Candy City,Gummy Worms': 150,
              'Exotic Extras,Kimchi and Seaweed': 799}

one_line_item.drop(columns = ['transaction_value'], inplace = True)

one_line_item['amount'] = one_line_item['item'].map(price_dict)

one_line_item['quantity'] = one_line_item['quantity'].astype(int)
one_line_item['amount'] = one_line_item['amount'].astype(int)

one_line_item['total_amount'] = one_line_item['quantity'] * one_line_item['amount']

one_line_item['total_amount'] = one_line_item['total_amount'].astype(int)
pivot2 = one_line_item.pivot_table(index=['transaction year', 'transaction month','item'], values=['total_amount'], aggfunc='sum')

dfi.export(pivot2,"PivotTable2.png")

def age_bucket(age):
    if age <= 18:
        return "<18"
    else:
        return ">18"
  
one_line_item['age group'] = one_line_item['age'].apply(age_bucket)

gender = pd.DataFrame(one_line_item.sex.value_counts(normalize=True)*100).reset_index()
gender.columns = ['sex', '%sex']
one_line_item = pd.merge(left=one_line_item, right=gender, how='inner', on=['sex'])
  

pivot3 = pd.pivot_table(one_line_item, index=['sex', '%sex', 'age group'], 
                       values=['address'], aggfunc={'address': 'count',})

print(pivot3)

dfi.export(pivot3,"PivotTable3.png")

group = one_line_item.groupby('address')
group['address'].count().sort_values(ascending=False).head(50)

top_50_addresses = pd.DataFrame(group['address'].count().sort_values(ascending=False).head(50))

dfi.export(top_50_addresses,"PivotTable4.png")

with open('transaction-data-adhoc-analysis.json', 'r') as f:
    data = json.load(f)
    
dataframe = pd.DataFrame(data)

dataframe['transaction_date'] = pd.to_datetime(dataframe['transaction_date'], format="%Y/mm/dd")

customers_per_month = dataframe.groupby(['name',dataframe['transaction_date'].dt.month.rename('transaction_month')])['transaction_value'].sum().reset_index()

customers_per_month.groupby('transaction_month')['name'].count()

number = pd.crosstab(customers_per_month['name'], customers_per_month['transaction_month'])

repeaters_01 = 0
repeaters_0102 = number[(number[1]>0)&(number[2]>0)][2].count() 
repeaters_0203 = number[(number[2]>0)&(number[3]>0)][3].count()
repeaters_0304 = number[(number[3]>0)&(number[4]>0)][4].count()
repeaters_0405 = number[(number[4]>0)&(number[5]>0)][5].count()
repeaters_0506 = number[(number[5]>0)&(number[6]>0)][6].count()

inactive_01 = 0
inactive_02 = number[(number[1]==0)&(number[2]>0)][2].count()
inactive_03 = number[(number[3]==0)&((number[1]>0)|(number[2]>0))][3].count()
inactive_04 = number[(number[4]==0)&((number[1]>0)|(number[2]>0)|(number[3]>0))][4].count()
inactive_05 = number[(number[5]==0)&((number[1]>0)|(number[2]>0)|(number[3]>0)|(number[4]>0))][5].count()
inactive_06 = number[(number[6]==0)&((number[1]>0)|(number[2]>0)|(number[3]>0)|(number[4]>0)|(number[5]>0))][6].count()

engaged_01 = number[(number[1]>0)][1].count()
engaged_02 = number[(number[1]>0)&(number[2]>0)][2].count()
engaged_03 = number[(number[1]>0)&(number[2]>0)&(number[3]>0)][3].count()
engaged_04 = number[(number[1]>0)&(number[2]>0)&(number[3]>0)&(number[4]>0)][4].count()
engaged_05 = number[(number[1]>0)&(number[2]>0)&(number[3]>0)&(number[4]>0)&(number[5]>0)][5].count()
engaged_06 = number[(number[1]>0)&(number[2]>0)&(number[3]>0)&(number[4]>0)&(number[5]>0)&(number[6]>0)][6].count()

dataset = np.array([[repeaters_01, repeaters_0102,repeaters_0203, repeaters_0304, repeaters_0405, repeaters_0506],
                  [inactive_01, inactive_02, inactive_03, inactive_04, inactive_05, inactive_06],
                  [engaged_01, engaged_02, engaged_03, engaged_04, engaged_05, engaged_06]])

table = pd.DataFrame(data = dataset, 
                        index = ['repeaters', 'inactive', 'engaged'],
                        columns = ['January/01', 'February/02', 'March/03', 'April/04', 'May/05', 'June/06'])

dfi.export(table,"Table1.png")

duplicated_names = customers_per_month.pivot_table(columns=['name'], aggfunc='size')

top_100_customers = pd.DataFrame(duplicated_names.sort_values(ascending=False).head(100))

dfi.export(top_100_customers,"Table2.png")