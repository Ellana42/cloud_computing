#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score


movies_data=pd.read_csv('movies.dat', sep = '::', engine='python', encoding='utf-8')
movies_data.head()
movies_data.columns =['MovieIDs','MovieName','Category']
movies_data.dropna(inplace=True)
movies_data


# In[65]:


pip install seaborn


# In[2]:




movies_data.dropna(inplace=True)
movies_data
all_categories={}
for i , row in movies_data.iterrows(): 
    ara= row['Category'].split("|")
    for j in ara : 
        if not j in all_categories.keys(): 
            all_categories[j]=[]
        
print(len(all_categories.keys()))


# In[3]:


for i , row in movies_data.iterrows(): 
    ara= row['Category'].split("|")
    for j in all_categories.keys():
        if j in ara :
            all_categories[j].append(1)
        else :
            all_categories[j].append(0)
for k in all_categories.keys(): 
    print(len(all_categories[k]))
print(all_categories.keys())


# In[4]:


for k in all_categories.keys(): 
    movies_data[k]=all_categories[k]


# In[5]:


# Remove column name 'A'
movies_data.drop(['Category'], axis = 1)


# In[6]:


rating_data = pd.read_csv("ratings.dat",sep='::', engine='python')
rating_data.columns =['ID','MovieID','Ratings','TimeStamp']
rating_data.dropna(inplace=True)


# In[10]:


df = pd.concat([movies_data, rating_data,user_data], axis=1)


# In[11]:


df.dropna(inplace=True)
gender=[]
#1 for male 0 for female
for j,row in df.iterrows(): 
    if row['Gender']=='M':
        gender.append(1)
    else :
        gender.append(0)
df.drop(['Gender'], axis = 1)
df['Gender']=gender


# In[12]:


user_data = pd.read_csv("users.dat",sep='::',engine='python')
user_data.columns =['UserID','Gender','Age','Occupation','Zip-code']
user_data.dropna(inplace=True)
user_data.drop(['Zip-code'], axis = 1)


# In[13]:



import seaborn as sns # For creating plots
c=df.corr()
plt.figure(figsize=(20,8))
sns.heatmap(c,annot=True)


# In[15]:


plt.figure(figsize=(15,8))
df.corr()['Ratings'].sort_values(ascending = False).plot(kind='bar')


# In[16]:


df.isnull().sum()


# In[26]:


training_data, testing_data = train_test_split(df, test_size=0.2)
y_train=training_data['Ratings']

X_train=training_data[['MovieID','Age','Occupation','Adventure', "Children's", 'Fantasy', 'Comedy', 'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror', 'Animation', 'Sci-Fi', 'Documentary', 'War', 'Musical', 'Mystery', 'Film-Noir', 'Western']].values
regr = linear_model.LinearRegression()
X_test=testing_data[['MovieID','Age','Occupation','Adventure', "Children's", 'Fantasy', 'Comedy', 'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror', 'Animation', 'Sci-Fi', 'Documentary', 'War', 'Musical', 'Mystery', 'Film-Noir', 'Western']].values
#X_test=testing_data.drop(['TimeStamp','Zip-code','MovieName','Category'], axis = 1)
y_test=testing_data['Ratings']
# Train the model using the training sets
regr.fit(X_train,y_train)
y_pred=regr.predict(X_test)

# Make predictions using the testing set
y_pred


# In[24]:


y_pred


# In[28]:


from sklearn.metrics import r2_score
r2_score(y_test,y_pred)

#on obtient un coefficient R2 trés faible, le modèle de régression linéaire n'est pas adapté
#on va tester un autre modèle


# In[32]:


from sklearn.tree import DecisionTreeClassifier
training_data, testing_data = train_test_split(df, test_size=0.2)
y_train=training_data['Ratings']

X_train=training_data[['MovieID','Age','Occupation','Adventure', "Children's", 'Fantasy', 'Comedy', 'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror', 'Animation', 'Sci-Fi', 'Documentary', 'War', 'Musical', 'Mystery', 'Film-Noir', 'Western']].values
regr = linear_model.LinearRegression()
X_test=testing_data[['MovieID','Age','Occupation','Adventure', "Children's", 'Fantasy', 'Comedy', 'Romance', 'Drama', 'Action', 'Crime', 'Thriller', 'Horror', 'Animation', 'Sci-Fi', 'Documentary', 'War', 'Musical', 'Mystery', 'Film-Noir', 'Western']].values
#X_test=testing_data.drop(['TimeStamp','Zip-code','MovieName','Category'], axis = 1)
y_test=testing_data['Ratings']
decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, y_train)
y_pred = decision_tree.predict(X_test)
acc_decision_tree = round(decision_tree.score(X_train, y_train) * 100, 2)

print("la précision du modèle est de")
acc_decision_tree

