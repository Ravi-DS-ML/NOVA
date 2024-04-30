import tensorflow as tf 
import numpy as np 
import pandas as pd 
import json 
from tensorflow import keras 
from keras.preprocessing.text import Tokenizer
import string
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import random
def get_data(prediction_input):
    with open('intents.json') as content:
        data = json.load(content)

    tags = []
    inputs = []
    responses_bots = {}

    for intent in data['intents']:
        responses_bots[intent['intent']] = intent['responses']
        for lines in intent['text']:
            inputs.append(lines)
            tags.append(intent['intent'])

    data = pd.DataFrame({'inputs':inputs, 'tags':tags})

    
    data['inputs'] = data['inputs'].apply(lambda wrd:[ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
    data['inputs'] = data['inputs'].apply(lambda wrd: ''.join(wrd))

    
    tokenizer = Tokenizer(num_words=2000)
    tokenizer.fit_on_texts(data['inputs'])
    train = tokenizer.texts_to_sequences(data['inputs'])

    
    X_train = pad_sequences(train)

    
    le = LabelEncoder()
    y_train = le.fit_transform(data['tags'])

    input_shape = X_train.shape[1]


    texts_p = []
    model = tf.keras.models.load_model('./model.h5')

        # removing Punctuations
    prediction_input = [ltrs.lower() for ltrs in prediction_input if ltrs not in string.punctuation]
    prediction_input = ''.join(prediction_input)
    texts_p.append(prediction_input)

        # tokenizing and padding
    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = pad_sequences([prediction_input],input_shape)

        #getting output from model
    output = model.predict(prediction_input)
    output = output.argmax()

        #finding the right tag and predicting
    response_tag = le.inverse_transform([output])[0]

    return random.choice(responses_bots[response_tag])

