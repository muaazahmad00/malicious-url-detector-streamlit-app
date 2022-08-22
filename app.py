import streamlit as st
import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle


# Tokenization
def makeTokens(f):
    tkns_BySlash = str(f.encode('utf-8')).split('/')	# make tokens after splitting by slash
    total_Tokens = []
    for i in tkns_BySlash:
        tokens = str(i).split('-')	# make tokens after splitting by dash
        tkns_ByDot = []
        for j in range(0,len(tokens)):
            temp_Tokens = str(tokens[j]).split('.')	# make tokens after splitting by dot
            tkns_ByDot = tkns_ByDot + temp_Tokens
        total_Tokens = total_Tokens + tokens + tkns_ByDot
    total_Tokens = list(set(total_Tokens))	#remove redundant tokens
    if 'com' in total_Tokens:
        total_Tokens.remove('com')	#removing .com since it occurs a lot of times and it should not be included in our features
    return total_Tokens

vectorizer = TfidfVectorizer()
model_path = 'logit.pkl'
vectorizer_path = 'vectorizer.pickle'
# Save the vectorizer
# vec_file = 'vectorizer.pickle'
# pickle.dump(vectorizer, open(vec_file, 'wb'))
loaded_vectorizer = pickle.load(open(vectorizer_path, 'rb'))

pickle_in = open(model_path, 'rb')
classifier = pickle.load(pickle_in)


st.sidebar.header('Malicious URL Detection App')
if not st.sidebar.checkbox("Hide", False, key='1'):
    st.title('Malicious URL Detector')
    url = st.text_input("Enter URL:")
submit = st.button('Detect')

if submit:
        loaded_vectorizer = pickle.load(open(vectorizer_path, 'rb'))
        input_data_transformed = loaded_vectorizer.transform([url])
        prediction = classifier.predict(input_data_transformed)

        if prediction == 'bad':
            st.write('Malicious')
        else:
            st.write('Not Malicious')