#!/usr/bin/env python
# coding: utf-8

# # GREATSCHOOLS.ORG API XML to CSV ETL Process
# ## This is a quick Python program to extract, parse API call responses from GreatSchool API (XML)
# ## Output is entered into a Pandas DataFrame, then ETL Processed:
# #### 1- remove unused columns
# #### 2 - normalize column names
# #### 3 - filter types to public school only
# #### 4 - add calculated columns for statistical analysis

# In[1]:


# Import Dependency
import requests
import pandas as pd
from config import api_key

from io import StringIO, BytesIO
from lxml import etree as et

# import Zip code list for greater Austin-Round Rock Metro area
csv_reader = pd.read_csv('zip-list.csv')
zip_df = pd.DataFrame(csv_reader)
zipList = list(zip_df.Zip)


# In[2]:


# API prep
url = 'https://api.greatschools.org/schools/nearby?'
queryURL = url + 'key=' + api_key + '&state=TX' + '&zip='

# print(queryURL)   


# In[3]:


# Process API Call response from XML into DataFrame
df1 = pd.DataFrame()
#tree = et.parse(xml)
#root = ElementTree(xml.content)

# build a series
d = {}

for zip in zipList:
    queryURL1 = queryURL + str(zip)
    # print('Processing: ' + queryURL1)
    xml = requests.get(queryURL1)
    tree = et.fromstring(xml.content)
    for child in tree:
        for children in child:
            d[str(children.tag)] = str(children.text)
        df1 = df1.append(d, ignore_index=True)

df1.head()


# In[4]:


# drop duplicates, keep one row
df1.drop_duplicates(subset='name', keep='last', inplace=True)
df1 = df1.dropna()


# In[5]:


df2 = pd.DataFrame()
#df2 = df1.loc[df1['type'] == 'public']

df2 = df1

df2.reset_index(drop=True, inplace=True)


# In[6]:


# check record integrity
df2.describe().T


# In[7]:


# list all columns
list(df2)


# In[8]:


# check record consistency
df2.count()


# In[9]:


# final report selected columns and calculated column
df3 = pd.DataFrame()
df3['ID'] = df2['gsId']
df3['Name'] = df2['name']
df3['Type'] = df2['type']
df3['City'] = df2['city']
df3['Zip'] = df2['address'].str[-5:]
df3['Grade'] = df2['gradeRange']
df3['Rating1'] = df2['gsRating']
df3['Rating2'] = df2['parentRating']
df3['RatingAll'] = pd.to_numeric(df3['Rating1'])*1.1 + pd.to_numeric(df3['Rating2'])*0.5
df3['lat'] = df2['lat']
df3['lon'] = df2['lon']
df3['Enrollment'] = df2['enrollment']

df3.reset_index(inplace=True)

df3.to_csv('GreatSchools_dataset.csv',index=False)


# In[10]:


df3.head()


# In[ ]:


get_ipython().system('jupyter nbconvert --to Python Great')

