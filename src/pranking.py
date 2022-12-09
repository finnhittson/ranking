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

	# weights and bias initialized to zero
	w = np.zeros((1, len(reviews) - 1))
	b = np.zeros((1, 10))

	for _ in range(cycles):

		# random viewer to be the true labels
		random_viewer = int(random.uniform(0,len(reviews)))
		np.random.shuffle(reviews)
		
		target_rank = copy.copy(reviews[random_viewer, :]) * 2# true labels
		reviews = np.delete(reviews,random_viewer,0) # rest of the data
		for idx, x in enumerate(reviews.T):

			# x is the set of reviews from different people
			w_dot_x = w.dot(np.array([x]).T)[0][0]
			predicted_rank = predict_rank(w_dot_x, b)

			# if predicted rank is wrong then update w and b
			if target_rank[idx] != predicted_rank:
				
				correction_vect = []
				for r in range(len(b[0])):
					if target_rank[idx] <= r:
						correction_vect.append(-1)
					else:
						correction_vect.append(1)
				
				tau = []
				for r in range(len(b[0])):
					if (w_dot_x - b[0][r]) * correction_vect[r] <= 0: # incorrect
						tau.append(correction_vect[r])
					else: # correct
						tau.append(0)
				
				# update w and b
				w = w + sum(tau) * x / 100
				for r in range(len(b[0])):
					b[0][r] = b[0][r] - tau[r]

		# re-append target ranks to total data set
		reviews = np.concatenate((reviews, np.array([target_rank])), axis=0)
	
	return w, b


# finds minimum rank
def predict_rank(w_dot_x, b):
	yt_hat = 10 # max rank
	r = 0
	while r < len(b[0]):
		if w_dot_x - b[0][r] < 0 and r < yt_hat:
			yt_hat = r
		r += 1
	return yt_hat


# runs and evaluates pranking algorithm
def run_pranking(data_path, review_count):

	# get data
	train_reviews = np.array(util.get_n_reviews(data_path, review_count))
	#util.write_to_file(train_reviews, 'data/100_quick.csv')
	
	# train
	w, b = pranking(train_reviews, 500)
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
	print("\nAccuracy {}%".format(correct_count))


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

  start = time.time()
  run_pranking(args.path, args.review_count)
  end = time.time()
  print(f'elapsed: {end - start}')