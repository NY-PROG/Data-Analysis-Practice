#!/usr/bin/env python
# coding: utf-8

# # Analysis of Uniqlo Sales

# Uniqlo is the core brand of Japan's Fast Retailing Company, founded in 1984 as a small clothing store selling suits. Uniqlo has become an internationally renowned clothing brand. Tadashi Yanai, the current chairman and general manager of Uniqlo, introduced the hypermarket style of clothing sales in Japan for the first time, and realized the low cost of store operation through a unique system of commodity planning, development and sales, thus leading to the hot selling trend of Uniqlo.

# In this analysis, I will analyze the sales data of Uniqlo in China. Explore how sales have changed over time, how different products have sold, how customers prefer to buy, and the relationship between sales and product costs.

# # Imports

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


uniqlo = pd.read_csv(r"/Users/ny/Desktop/数据分析训练/zuoyeweek1.unique.csv")


# # Basic Info

# In[3]:


uniqlo.info()


# In[4]:


uniqlo.head()


# In[5]:


uniqlo.describe()


# # Data Cleaning

# In[6]:


import numpy as np
uniqlo.loc[uniqlo.age_group =='Unknown','age_group']=np.nan
uniqlo.loc[uniqlo.gender_group =='Unknown','gender_group']=np.nan 


# In[7]:


uniqlo.isnull().sum()/len(uniqlo)


# In[8]:


uniqlo.dropna()


# In[9]:


uniqlo.drop('store_id',axis=1,inplace=True)


# In[10]:


uniqlo.describe()


# Clean the max of revenue.

# In[11]:


uniqlo.revenue.value_counts()


# In[12]:


bins=[-1000,0,100,500,1000,2000,5000,10000,15000]
uniqlo['revenue_level']=pd.cut(uniqlo.revenue, bins,right=False)


# In[13]:


uniqlo.groupby('revenue_level').revenue.describe()


# In[14]:


uniqlo= uniqlo[(uniqlo.revenue>0)&(uniqlo.revenue<2000)]
uniqlo.revenue.describe()


# In[15]:


uniqlo.describe()


# # Relationships between revenue and time points

# In[16]:


uniqlo.groupby('wkd_ind').revenue.sum()


# In[17]:


( 1398312.33)/(1927993.60/5)


# In[18]:


uniqlo.groupby('wkd_ind').customer.sum()


# In[19]:


(14626/2)/(20378/5)


# In[20]:


uniqlo.groupby('wkd_ind').revenue.sum()/uniqlo.groupby('wkd_ind').customer.sum()


# In[21]:


sns.barplot(x='wkd_ind',y='revenue',data=uniqlo)


# In[22]:


uniqlo.groupby('wkd_ind').revenue.describe()


# There were more weekday customers than weekend customers, and average revenues were almost same. 
# More promotional activities should be carried out on weekends to attract more customers.

# # Product sales

# In[23]:


plt.rcParams['font.sans-serif']=['Arial Unicode MS']
plt.rcParams['axes.unicode_minus']=False
sns.barplot(x='product',y='revenue',data=uniqlo)


# In[24]:


uniqlo.groupby('product').revenue.describe()


# In[25]:


uniqlo.groupby('product').revenue.mean().sort_values(ascending=False).index


# In[26]:


sns.barplot(x='product',y='revenue',data=uniqlo, 
            order=uniqlo.groupby('product').revenue.mean().sort_values(ascending=False).index)


# In[27]:


sns.barplot(y='revenue',x='product',data=uniqlo,estimator=sum,
            order=uniqlo.groupby('product').revenue.sum().sort_values(ascending=False).index)


# Sweaters have the highest average sales volume and T-shirts have the highest total sales price,
# probably because T-shirts are cheap and sweaters are expensive

# # Purchase channels

# In[28]:


sns.barplot(x='city',y='revenue',hue='channel', data=uniqlo, estimator=sum, order=uniqlo.groupby('city').revenue.sum().sort_values(ascending=False).index)


# In[29]:


sns.barplot(x='gender_group',y='revenue',hue='channel', data=uniqlo, estimator=sum, order=uniqlo.groupby('gender_group').revenue.sum().sort_values(ascending=False).index)


# In[30]:


sns.barplot(x='gender_group',y='revenue',hue='channel', data=uniqlo, order=uniqlo.groupby('gender_group').revenue.mean().sort_values(ascending=False).index)


# In[31]:


sns.barplot(x='age_group',y='revenue',hue='channel', data=uniqlo, estimator=sum, order=uniqlo.groupby('age_group').revenue.sum().sort_values(ascending=False).index)


# In big cities such as Beijing and Shanghai, the online sales data are missing, 
# and the purchase rate of the whole population is higher offline than online. 
# Women are generally more likely to buy online than men. 
# Online and offline purchases are concentrated between 20 and 40 years old

# # Relationship between sales and product costs

# In[32]:


uniqlo['unit_revenue']= uniqlo.revenue/uniqlo.quant
uniqlo['margin']=uniqlo.unit_revenue-uniqlo.unit_cost
uniqlo.head()


# In[33]:


sns.barplot(y='margin',x='product',data=uniqlo,order=uniqlo.groupby('product').margin.mean().sort_values(ascending=False).index)


# In[34]:


q=['margin','unit_revenue','unit_cost']
uniqlo[q].corr()


# In[35]:


sns.heatmap(uniqlo[q].corr())


# In[36]:


bins = [-100,-25,0,25,50,100,150,200]
uniqlo['margin_level']=pd.cut(uniqlo.margin, bins, right=False)
uniqlo.groupby('margin_level').margin.describe()


# In[37]:


fig=plt.figure(figsize=(20,10))
sns.barplot(x='product',y='quant',hue='margin_level',estimator=sum,data=uniqlo)


# Some jeans are showing negative margin. Tshirts are often sold in large quantities but with a small profit
