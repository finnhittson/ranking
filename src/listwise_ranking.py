import argparse
import util
import ann
import math
import random
import numpy as np
import time
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

def listwise_ranking(X, y, alpha, tolerance):
	W1, b1, W2, b2 = ann.initialize_parameters()
	likelihood_loss = math.inf
	iterations = 0
	clf = MLPClassifier(solver="lbfgs", alpha=1e-5, hidden_layer_sizes=(3,), random_state=1, max_iter=1)
	while likelihood_loss > tolerance and iterations < 100:
		for idx, x in enumerate(X):
			#clf.fit([x],[y[idx]])
			W1, b1, W2, b2 = ann.compute_gradient(np.array([x]).T, y[idx], W1, b1, W2, b2, alpha)
		likelihood_loss = compute_likelihood_loss(clf, W1, b1, W2, b2, X, y)
		if iterations % 10 == 9 or False:
			print("Likelihood Loss: {}".format(likelihood_loss))
		iterations += 1
	return W1, b1, W2, b2 #clf


def compute_likelihood_loss(clf, W1, b1, W2, b2, X, y):
	p_y_xg = 1
	for i, x in enumerate(X):
		_, A2 = ann.forward_propagation(W1, b1, W2, b2, np.array([x]).T)
		#gi = math.exp(clf.predict([x]))
		gi = math.exp(ann.get_predictions(A2)[0])
		rolling_sum = 0
		k = i
		while k < len(X):
			_, A2 = ann.forward_propagation(W1, b1, W2, b2, np.array([X[k]]).T)
			rolling_sum += math.exp(ann.get_predictions(A2)[0])
			#rolling_sum += math.exp(clf.predict([X[k]]))
			k += 1
		p_y_xg -= math.log(gi) - math.log(rolling_sum)
	return p_y_xg


def run_listwise_ranking(data_path):
	X, y = util.get_queries(data_path)
	#print(len(y))
	#X_train, y_train, X_test, y_test = util.split_queries(X, y, 0.2)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
	'''
	scaler = preprocessing.StandardScaler().fit(X_train)
	X_scaled = scaler.transform(X_train)
	alpha = 0.001
	tolerance = 0.3
	clf = listwise_ranking(X_scaled, y_train, alpha, tolerance)
	return
	'''
	alpha = 0.001
	tolerance = 0.3
	W1, b1, W2, b2 = listwise_ranking(X, y, alpha, tolerance)
	return
	correct_count = 0
	prediction = []
	#print(y_test)
	for idx, x in enumerate(X_test):
		_, A2 = ann.forward_propagation(W1, b1, W2, b2, np.array([x]).T)
		prediction.append(ann.get_predictions(A2)[0])
		if prediction[-1] == y_test[idx]:
			correct_count += 1
	print(y_test)
	print(prediction)
	print(f"{correct_count / len(y_test) * 100}%")
	

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Run listwise ranking algorithm')
	parser.add_argument(
		'path',
		metavar='PATH',
		type=str,
		help='Path to the data.')
	parser.add_argument(
		'--use-relu',
		dest='relu',
		action='store_false',
		help='Use ReLU activation function instead of sigmoid.')
	parser.set_default(relu = False)
	args = parser.parse_args()
	
	start = time.time()
	run_listwise_ranking(args.path)
	end = time.time()
	print(f"elapsed: {end - start}")