'''
Script to clean the online recruitment fraud dataset
and vectorize it for training
'''

# Import the libraries needed
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import re
from sklearn.feature_extraction.text import CountVectorizer

# Load the dataset
jobs_df = pd.read_csv("emscad_v1.csv")

# Deal with missing values and drop unneccessary columns

# Location missing values will be assigned none
jobs_df['location'] = jobs_df.location.fillna('none')

# department missing values will be assigned not specified
jobs_df['department'] = jobs_df.department.fillna('not specified')

# drop salary range, benefits, telecommuting, has_questions (not compulsory) in the context of Nigeria
jobs_df.drop(['salary_range', 'benefits','telecommuting', 'in_balanced_dataset','has_questions'],
             axis=1, inplace=True)

# Company profile missing values will be assigned none
jobs_df['company_profile'] = jobs_df.company_profile.fillna('none')

# Company profile missing values will be assigned not specified
jobs_df['requirements'] = jobs_df.requirements.fillna('not specified')

# employment_type missing values will be assigned not specified
jobs_df['employment_type'] = jobs_df.employment_type.fillna('not specified')

# required_experience missing values will be assigned not specified
jobs_df['required_experience'] = jobs_df.required_experience.fillna('not specified')

# required_education missing values will be assigned not specified
jobs_df['required_education'] = jobs_df.required_education.fillna('not specified')

# industry missing values will be assigned not specified
jobs_df['industry'] = jobs_df.industry.fillna('not specified')

# function missing values will be assigned not specified
jobs_df['function'] = jobs_df.function.fillna('not specified')

# Remove html tags
jobs_df['company_profile'] = jobs_df.company_profile.str.replace(r'<[^>]*>', '')
jobs_df['description'] = jobs_df.description.str.replace(r'<[^>]*>', '')
jobs_df['requirements'] = jobs_df.requirements.str.replace(r'<[^>]*>', '')

# Remove non word characters and trailing white space 
for column in jobs_df.columns:
    jobs_df[column] = jobs_df[column].str.replace(r'\W', ' ').str.replace(r'\s$','')

# Encode binary columns t as 1 and f as 0
jobs_df['has_company_logo'] = jobs_df.has_company_logo.map({'t': 1, 'f':0})
jobs_df['fraudulent'] = jobs_df.fraudulent.map({'t': 1, 'f':0})

vect = CountVectorizer()

def clean_series(column_name):
    jobs_df[column_name] = jobs_df[column_name].apply(lambda x: " ".join([i for i in x.lower().split() if i not in stop_words]))

text_columns = ['title', 'location', 'department', 'company_profile', 'description', 'requirements','employment_type','required_experience','required_education','industry','function']
for column in text_columns:
    clean_series(column)

# creates a function that will use TFIDF vectorizer to vectorize all text data
from sklearn.feature_extraction.text import TfidfVectorizer

# initialize the vectorizer
vectorizer = TfidfVectorizer()

def vectorize_data(column):
    jobs_df[column] = list(vectorizer.fit_transform(jobs_df[column]))
text_columns = ['title','location', 'department', 'company_profile', 'description', 'requirements','employment_type','required_experience','required_education','industry','function']

# Loop through the text columns and vectorize each
for column in text_columns:
    vectorize_data(column)