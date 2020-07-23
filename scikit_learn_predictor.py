import pickle

# load the model from local file
clf = pickle.load(open('skt-learn-model.pkl', 'rb'))

"""
features: two dimensional array,[[1,2,3]], here we just pass one item for predicting
return : call the model predict function.
         note: return an array and each item represents the predicting result of the input data, here we just get the
         first value.        
"""


def predict(features):
    return clf.predict(features)[0]
