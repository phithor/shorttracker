
# coding: utf-8

# # Code to retreive Short Register of Norwegian Stocks and Graph result

# In[1]:


import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')
get_ipython().run_line_magic('matplotlib', 'notebook')


# In[2]:


df = pd.read_json("https://ssr.finanstilsynet.no/api/Issuers?extension=json")

df.head()


# In[3]:


df_test = pd.DataFrame(df['Positions'][4])
print(df['Name'][3])
idxs = pd.date_range(df_test['ShortingDate'].min(), df_test['ShortingDate'].max())
df_values = pd.DataFrame(index=idxs)
for idx in reversed(df_test.index):
    #print(idx, df_test.loc[idx, 'PositionHolder'], df_test.loc[idx, 'ShortPercent'])
    if df_test.loc[idx, 'PositionHolder'] not in df_values.columns:
        df_values[df_test.loc[idx, 'PositionHolder']] = np.nan
        
    #df_values[df_test.loc[idx, 'PositionHolder']]
    if df_test.loc[idx, 'Status'] == 2:
        df_values.loc[df_test.loc[idx, 'ShortingDate'], df_test.loc[idx, 'PositionHolder']] = df_test.loc[idx, 'ShortPercent']
    
#df_values['Total'] = df_values.sum(axis=1)
#df_values
df_fixed = df_values
one_day = timedelta(days=1)
for coloumn in df_fixed.columns:
    for idx, value in df_fixed[coloumn].iteritems():
        #print(idx)
        #print(df_fixed[coloumn].loc[idx])
        if pd.isnull(df_fixed[coloumn].loc[idx]) and idx != df_fixed.index.values[0]:
            #print(df_fixed[coloumn].loc[idx])
            df_fixed[coloumn].loc[idx] = df_fixed[coloumn].loc[idx-one_day]
            

df_fixed['Total'] = df_values.sum(axis=1)
print(df_fixed.iloc[-1,:])
#print(df_fixed.tail())


data = df_fixed['Total']



data.plot()


    

