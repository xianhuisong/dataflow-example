from sklearn.ensemble import RandomForestClassifier
import pickle

"""
use the scikit-learn to train the RandomForestClassifier
see https://scikit-learn.org/stable/modules/ensemble.html#forest 
"""
clf = RandomForestClassifier(random_state=0)
# this is the training data, two rows, and three features
X = [[1, 2, 3], [11, 12, 13]]
# this is the label
y = [0, 1]
clf.fit(X, y)
# save the model to the local file
pickle.dump(clf, open('skt-learn-model.pkl', 'wb'))
