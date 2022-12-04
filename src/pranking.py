import argparse
import util
import math
import random
import numpy as np
import copy
import time
import matplotlib.pyplot as plt


# pranking algorithm
def pranking(reviews, cycles):
	reviews = np.array(reviews)
	w = np.zeros((len(reviews) - 1, 1)) # weights and bias initialized to zero
	b = [0, 0, 0, 0, 0]

	for _ in range(cycles):

		# random viewer to be the true labels
		random_viewer = int(random.uniform(0,len(reviews)))
		np.random.shuffle(reviews)

		target_rank = copy.copy(reviews[random_viewer, :]) # true labels
		reviews = np.delete(reviews,random_viewer,0) # rest of the data

		for idx, x in enumerate(reviews.T):
			# x is the set of reviews from different people
			w_dot_x = w.dot(x)

			predicted_rank = predicted_rank(w_dot_x, b)
			
			# if predicted rank is wrong then update w and b
			if target_rank[idx] != predicted_rank / 2:
				
				correction_vect = []
				for r in range(len(b)):
					if target_rank[idx] <= r:
						correction_vect.append(-1)
					else:
						correction_vect.append(1)
				
				tau = []
				for r in range(len(b)):
					if (w_dot_x[0][0] - b[r]) * correction_vect[r] <= 0: # incorrect
						tau.append(correction_vect[r])
					else: # correct
						tau.append(0)
				
				# update w and b
				w = w + sum(tau) * x
				for r in range(len(b)):
					b[r] = b[r] - tau[r]
		
		# re-append target ranks to total data set
		reviews = np.concatenate((reviews, np.array([target_rank])), axis=0)
	
	return w, b


# finds minimum rank
def predict_rank(w_dot_x, b):
	yt_hat = 10 # max rank
	r = 0
	while r < len(b):
		if w_dot_x[0][0] - b[r] < 0 and r < yt_hat:
			yt_hat = r
		r += 1
	return yt_hat


# runs and evaluates pranking algorithm
def run_pranking(data_path, review_count):

	# get data
	train_reviews = np.array(util.get_n_reviews(data_path, review_count))
	#util.write_to_file(train_reviews, 'data/100_quick.csv')
	
	# train
	w, b = pranking(train_reviews,10)
	print(w)
	print(b)
	
	# evaluate
	correct_count = 0
	random_viewer = int(random.uniform(0,len(train_reviews)))
	true_ranks = copy.copy(train_reviews[random_viewer, :])
	train_reviews = np.delete(train_reviews, random_viewer, 0)
	predicted_rank = []
	
	for idx, review in enumerate(train_reviews.T):			
		predicted_rank.append(predict_rank(w.dot(review), b) / 2)

		if predicted_rank[-1] == true_ranks[idx]:
			correct_count += 1

	#print(np.array(predicted_rank)[:15])
	#print(true_ranks[:15])
	print("\n {}%".format(correct_count))


if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Run perceptron ranking algorithm')
  parser.add_argument(
		'path',
		metavar='PATH',
		type=str,
		help='The path to the data.')
  parser.add_argument(
  	'--review-count',
  	dest='review_count',
  	type=int,
  	help = 'Minimum movies reviewed')
  parser.set_defaults(review_count = 100)
  args = parser.parse_args()

  util.make_data(100, 100)

  #run_pranking(args.path, args.review_count)