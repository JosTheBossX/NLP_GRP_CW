import contractions
import spacy
import nltk
import pickle
import subprocess
import pandas as pd

from datetime import datetime
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from keras_preprocessing.sequence import pad_sequences

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

model_url = "https://huggingface.co/spacy/en_core_web_sm/resolve/main/en_core_web_sm-any-py3-none-any.whl"
subprocess.run(["pip", "install", model_url])
nlp = spacy.load("en_core_web_sm")

stop_words = set(stopwords.words('english'))


def text_transform(string_text):
    with open('model/tokenizer.pickle', 'rb') as handle:
        loaded_tokenizer = pickle.load(handle)
    string_text_list = []
    string_text_list.append(string_text)
    sequences = loaded_tokenizer.texts_to_sequences(string_text_list)
    padded_sequences = pad_sequences(sequences, maxlen=50, padding='post', truncating='post')
    return padded_sequences


# python -m spacy download en_core_web_sm
# pre-processing the data by getting verb, adj, adv; because of the emotion of sentence is depends on these character
import re


# pre-processing the data by getting verb, adj, adv; because of the emotion of sentence is depends on these character
def get_main_words(string_text):
    tokens = nltk.word_tokenize(string_text)
    pos_tags = nltk.pos_tag(tokens)

    pos_string = "{'JJR', 'VB', 'WP', 'WRB', 'NNS', 'JJS', 'JJ', 'RB', 'MD', 'VBZ', 'VBG', 'VBP'}"
    words = re.findall(r"'(\w+)'", pos_string)

    string_list = [token for token, tag in pos_tags if tag in words]

    if string_list:
        string_list = ' '.join(string_list)
        return string_list
    return None


# complex pre-processing data
def pre_processing_data_2(string_text):
    string_text = string_text.lower()
    string_output = ' '.join([token.lemma_ for token in nlp(string_text)])
    string_output = contractions.fix(string_output)

    string_processed = get_main_words(string_output)
    if string_processed:
        tokenizer = RegexpTokenizer(r'\w+')
        string_processed = tokenizer.tokenize(string_processed)
        string_processed = " ".join(string_processed)
        return string_processed

    tokenizer = RegexpTokenizer(r'\w+')
    string_output = tokenizer.tokenize(string_output)
    string_output = [w for w in string_output if not w in stop_words]
    string_output = " ".join(string_output)
    return string_output


def preprocessing_data(string_text):
    string_text = string_text.lower()
    string_output = ' '.join([token.lemma_ for token in nlp(string_text)])
    string_output = contractions.fix(string_output)

    tokenizer = RegexpTokenizer(r'\w+')
    string_output = tokenizer.tokenize(string_output)
    string_output = [w for w in string_output if not w in stop_words]
    string_output = " ".join(string_output)
    return string_output


def user_capture(user_input, emotion_prd):
    dataframe_capture = pd.read_csv('user_logs.csv')
    user_input_logs = pd.DataFrame({
        "user_input": [user_input],
        "emotion_predict": [emotion_prd],
        "time_logs": [datetime.now()],
    })

    dataframe_capture = pd.concat([dataframe_capture, user_input_logs], ignore_index=True)
    dataframe_capture.to_csv("user_logs.csv", index=False)
    print("Done Recorded")
    return None
