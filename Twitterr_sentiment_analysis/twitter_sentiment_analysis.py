# -*- coding: utf-8 -*-
"""Twitter_Sentiment_Analysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oL_r3Ca6p_q4RRF77BHJOg26-dj2kPG3
"""

#configuring the path of kaggle.json file
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!chmod 600 ~/.kaggle/kaggle.json

"""Now we will Download the Dataset from kaggle"""

#API to fetch the dataset from Kaggle
!kaggle datasets download -d jp797498e/twitter-entity-sentiment-analysis

#extracting the zip file
from zipfile import ZipFile
dataset='/content/twitter-entity-sentiment-analysis.zip'

with ZipFile(dataset, 'r') as zip:
  zip.extractall()

"""Now we need to Import the Dependencies for our Project."""

import numpy as np
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import nltk
nltk.download('stopwords')

#print stopwords in English
print(stopwords.words('english'))

#loading data from csv file to panda dataframe
twitter_data= pd.read_csv('/content/twitter_training.csv', encoding ='ISO-8859-1')

# Number of rows and columns
twitter_data.shape

#printing first 5 rows of dataframe
twitter_data.head()

#naming column dataset
column_names= ['Tweet_id','Entity','The polarity of the tweet','tweet_content']
twitter_data= pd.read_csv('/content/twitter_training.csv',names= column_names, encoding ='ISO-8859-1')

twitter_data.shape

twitter_data.head()

#Check for missing values in the dataset
twitter_data.isnull().sum()

twitter_data[twitter_data['tweet_content'].isna() == True]

# dropping the rows as it has no review written in body
twitter_data.dropna(inplace=True)

twitter_data.isnull().sum()

#check for target distribution
twitter_data['The polarity of the tweet'].value_counts()

# dropping the irrelevant columns
twitter_data.drop(twitter_data[twitter_data['The polarity of the tweet'] == 'Irrelevant'].index, inplace=True)

print(twitter_data['The polarity of the tweet'].value_counts())

twitter_data.replace({'The polarity of the tweet': {'Positive': 1, 'Negative': -1, 'Neutral': 0}}, inplace=True)

twitter_data['The polarity of the tweet'].value_counts()

"""-1--> Negative 0--> Neutral 1--> Positive

Stemming: The process of reducing a word to its root word eg. act is root word for actor, acting.
"""

port_stem = PorterStemmer()

def stemming(content):

  stemmed_content= re.sub('[^a-zA-Z]',' ',content)
  stemmed_content= stemmed_content.lower()
  stemmed_content= stemmed_content.split()
  stemmed_content= [port_stem.stem(word) for word in stemmed_content if not word in stopwords.words('english')]
  stemmed_content = ' '.join(stemmed_content)

  return stemmed_content

# Filter rows where 'tweet_content' is NaN
twitter_data['stemmed_content']= twitter_data['tweet_content'].apply(stemming)

twitter_data.head()

print(twitter_data['stemmed_content'])

print(twitter_data['The polarity of the tweet'])

#seperating the data and label

X= twitter_data['stemmed_content'].values
Y= twitter_data['The polarity of the tweet'].values

print(X)

# Convert variable Y to a list and print it
print(Y.tolist())

"""Splitting the data to training data and test data"""

# Split dataset X and target variable Y into training and testing sets,
# with a test size of 20%, stratify Y, and set random state to 2
X_train, X_test, Y_train, Y_test= train_test_split(X,Y, test_size=0.2, stratify= Y, random_state= 2)

print(X.shape, X_train, X_test.shape)

#feature extraction(converting textual data to numerical data)
vectorizer = TfidfVectorizer()

X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

print(X_train)

print(X_test)

"""Training the Machine Learning Model

Logistic Regression
"""

model= LogisticRegression(max_iter=2000)

model.fit(X_train, Y_train)

"""Model Evaluation

Accuracy Score
"""

#accuracy score on training data
X_train_prediction = model.predict(X_train)
training_data_accuracy= accuracy_score(Y_train, X_train_prediction)

print('Accuracy score on training data: ', training_data_accuracy)

"""Model accuracy= 86.5%

Saving the Trained Model
"""

import pickle

filename= 'trained_model.pkl'
pickle.dump(model, open(filename,'wb'))

"""**Model Testing**"""

#loading the saved model
loaded_model = pickle.load(open('/content/trained_model.pkl','rb'))

X_new= X_test[3]
print(Y_test[3])

prediction = model.predict(X_new)
print(prediction)

if (prediction[0]==-1):
  print('Negative tweet')

if(prediction[0]==0):
  print('Neutral Tweet')

if(prediction[0]==1):
  print('Positive Tweet')

X_new= X_test[2]
print(Y_test[2])

prediction = model.predict(X_new)
print(prediction)

if (prediction[0]==-1):
  print('Negative tweet')

if(prediction[0]==0):
  print('Neutral Tweet')

if(prediction[0]==1):
  print('Positive Tweet')

X_new= X_test[8]
print(Y_test[8])

prediction = model.predict(X_new)
print(prediction)

if (prediction[0]==-1):
  print('Negative tweet')

if(prediction[0]==0):
  print('Neutral Tweet')

if(prediction[0]==1):
  print('Positive Tweet')

import pickle

# Load the trained model
loaded_model = pickle.load(open('/content/trained_model.pkl', 'rb'))

def predict_sentiment(input_text):
    # Preprocess the input text
    preprocessed_text = stemming(input_text)  # Assuming you have defined the 'stemming' function

    # Vectorize the preprocessed text
    vectorized_text = vectorizer.transform([preprocessed_text])

    # Predict the sentiment using the loaded model
    prediction = loaded_model.predict(vectorized_text)

    # Interpret the prediction
    if prediction[0] == -1:
        return 'Negative review'
    elif prediction[0] == 0:
        return 'Neutral review'
    elif prediction[0] == 1:
        return 'Positive review'

# Example usage
input_review = "very good"
sentiment_prediction = predict_sentiment(input_review)
print("Sentiment prediction:", sentiment_prediction)

