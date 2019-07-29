import nltk
import pandas as pd
import numpy as np
from glove import Glove
from sklearn.preprocessing import LabelEncoder
from sklearn import metrics
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import OneHotEncoder
from nltk.corpus import stopwords

labelEncoder = LabelEncoder()
one_enc = OneHotEncoder()
lemma = nltk.WordNetLemmatizer()

# Stopwords
extra_stopwords = [
    'also',
]
stop = stopwords.words('english') + extra_stopwords


def tokenize(text, min_len=1):
    '''Function that tokenize a set of strings
    Input:
        -text: set of strings
        -min_len: tokens length
    Output:
        -list containing set of tokens'''

    tokens = [word.lower() for sent in nltk.sent_tokenize(text)
              for word in nltk.word_tokenize(sent)]
    filtered_tokens = []

    for token in tokens:
        if token.isalpha() and len(token) >= min_len:
            filtered_tokens.append(token)

    return [x.lower() for x in filtered_tokens if x not in stop]


def tokenize_and_lemma(text, min_len=0):
    '''Function that retrieves lemmatised tokens
    Inputs:
        -text: set of strings
        -min_len: length of text
    Outputs:
        -list containing lemmatised tokens'''
    filtered_tokens = tokenize(text, min_len=min_len)

    lemmas = [lemma.lemmatize(t) for t in filtered_tokens]
    return lemmas


def get_vector(word, model, return_zero=False):
    '''Function that retrieves word embeddings (vector)
    Inputs:
        -word: token (string)
        -model: trained MLP model
        -return_zero: boolean variable
    Outputs:
        -wv: numpy array (vector)'''
    epsilon = 1.e-10

    unk_idx = model.dictionary['unk']
    idx = model.dictionary.get(word, unk_idx)
    wv = model.word_vectors[idx].copy()

    if return_zero and word not in model.dictionary:
        n_comp = model.word_vectors.shape[1]
        wv = np.zeros(n_comp) + epsilon

    return wv


def mean_embeddings(dataframe_file, model):
    '''Function to retrieve sentence embeddings from dataframe with
    lithological descriptions.
    Inputs:
        -dataframe_file: pandas dataframe containing lithological descriptions
                         and reclassified lithologies
        -model: word embeddings model generated using GloVe
    Outputs:
        -DF: pandas dataframe including sentence embeddings'''
    DF = pd.read_pickle(dataframe_file)
    DF = DF.drop_duplicates(subset=['x', 'y', 'z'])
    DF['tokens'] = DF['Description'].apply(lambda x: tokenize_and_lemma(x))
    DF['length'] = DF['tokens'].apply(lambda x: len(x))
    DF = DF[DF.length > 0]
    DF['vectors'] = DF['tokens'].apply(lambda x: np.asarray([get_vector(n, model) for n in x]))
    DF['mean'] = DF['vectors'].apply(lambda x: np.mean(x[~np.all(x == 1.e-10, axis=1)], axis=0))
    DF['reclass'] = pd.Categorical(DF.reclass)
    DF['code'] = DF.reclass.cat.codes
    DF['drop'] = DF['mean'].apply(lambda x: (~np.isnan(x).any()))
    DF = DF[DF['drop']]
    return DF


def split_stratified_dataset(Dataframe, test_size, validation_size):
    '''Function that split dataset into test, training and validation subsets
    Inputs:
        -Dataframe: pandas dataframe with sentence mean_embeddings
        -test_size: decimal number to generate the test subset
        -validation_size: decimal number to generate the validation subset
    Outputs:
        -X: numpy array with embeddings
        -Y: numpy array with lithological classes
        -X_test: numpy array with embeddings for test subset
        -Y_test: numpy array with lithological classes for test subset
        -Xt: numpy array with embeddings for training subset
        -yt: numpy array with lithological classes for training subset
        -Xv: numpy array with embeddings for validation subset
        -yv: numpy array with lithological classes for validation subset
        '''
    X = np.vstack(Dataframe['mean'].values)
    Y = Dataframe.code.values.reshape(len(Dataframe.code), 1)
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        Y,
                                                        test_size=test_size,
                                                        stratify=Y,
                                                        random_state=42)
    Xt, Xv, yt, yv = train_test_split(X_train,
                                      y_train,
                                      test_size=validation_size,
                                      stratify=None,
                                      random_state=1)
    return X, Y, X_test, y_test, Xt, yt, Xv, yv


def retrieve_predictions(classifier, x):
    '''Function that retrieves lithological classes using the trained classifier
    Inputs:
        -classifier: trained MLP classifier
        -x: numpy array containing embbedings
    Outputs:
        -codes_pred: numpy array containing lithological classes predicted'''
    preds = classifier.predict(x, verbose=0)
    new_onehot = np.zeros((x.shape[0], 18))
    new_onehot[np.arange(len(preds)), preds.argmax(axis=1)] = 1
    codes_pred = one_enc.inverse_transform(new_onehot)
    return codes_pred


def classifier_assess(classifier, x, y):
    '''Function that prints the performance of the classifier
    Inputs:
        -classifier: trained MLP classifier
        -x: numpy array with embeddings
        -y: numpy array with lithological classes predicted'''
    Y2 = retrieve_predictions(classifier, x)
    print('f1 score: ', metrics.f1_score(y, Y2, average='macro'),
          'accuracy: ', metrics.accuracy_score(y, Y2),
          'balanced_accuracy:', metrics.balanced_accuracy_score(y, Y2))


def save_predictions(Dataframe, classifier, x, name):
    '''Function that saves dataframe predictions as a pickle file
    Inputs:
        -Dataframe: pandas dataframe with mean_embeddings
        -classifier: trained MLP model,
        -x: numpy array with embeddings,
        -name: string name to save dataframe
    Outputs:
        -save dataframe'''
    preds = classifier.predict(x, verbose=0)
    Dataframe['predicted_probabilities'] = preds.tolist()
    Dataframe['pred'] = retrieve_predictions(classifier, x).astype(np.int32)
    Dataframe[['x', 'y', 'FromDepth', 'ToDepth', 'TopElev', 'BottomElev',
               'mean', 'predicted_probabilities', 'pred', 'reclass', 'code']].to_pickle('{}.pkl'.format(name))


# loading word embeddings model
# (This can be obtained from https://github.com/spadarian/GeoVec )
modelEmb = Glove.load('/home/ignacio/Documents/chapter2/best_glove_300_317413_w10_lemma.pkl')

# getting the mean embeddings of descriptions
DF = mean_embeddings('manualTest.pkl', modelEmb)

# subseting dataset for training classifier
X, Y, X_test, Y_test, X_train, Y_train, X_validation, Y_validation = split_stratified_dataset(DF, 0.1, 0.1)

# encoding lithological classes
encodes = one_enc.fit_transform(Y_train).toarray()

# MLP model generation
model = Sequential()
model.add(Dense(100, input_dim=300, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(100, activation='relu'))
model.add(Dense(units=len(DF.code.unique()), activation='softmax'))
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# training MLP model
model.fit(X_train, encodes, epochs=30, batch_size=100, verbose=2)

# saving MLP model
model.save('mlp_prob_model.h5')

# assessment of model performance
classifier_assess(model, X_validation, Y_validation)

# save lithological prediction likelihoods dataframe
save_predictions(DF, model, X, 'NSWpredictions')
