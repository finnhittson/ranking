import argparse
import util
import math
import random
import numpy as np

b = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

def pranking(reviews, cycles):
	reviews = np.array(reviews)

	for _ in range(cycles):
		random_viewer = int(random.uniform(0,len(reviews.T)))
		np.random.shuffle(reviews)
		target_rank = reviews[:,random_viewer]
		reviews = np.delete(reviews,random_viewer,1)

		w = np.array([0] * len(reviews))
		b = [0] * 10
		len_b = len(b)

		for idx, review in enumerate(reviews.T):
			
			w_dot_x = w.dot(review)
			predicted_rank = predict_rank(w_dot_x, b)
			
			if target_rank[idx] != predicted_rank:
				
				correction_vect = []
				for r in range(len_b):
					if math.floor(target_rank[idx]*2) <= r:
						correction_vect.append(-1)
					else:
						correction_vect.append(1)

				tau = []
				for r in range(len_b):
					if (w_dot_x - b[r]) * correction_vect[r] <= 0: # incorrect
						tau.append(correction_vect[r])
					else: # correct
						tau.append(0)

				w = w + sum(tau) * review
				for t in range(len_b):
					b[t] = b[t] - tau[t]

		reviews = np.concatenate((reviews, np.array([target_rank]).T), axis=1)
	
	return w, b

def predict_rank(w_dot_x, b):
	yt_hat = math.inf
	rank_idx = 0
	while rank_idx < len(b):
		if w_dot_x - b[rank_idx] < 0 and rank_idx < yt_hat:
			yt_hat = rank_idx
		rank_idx += 1
	return yt_hat

def run_pranking(data_path, review_count):
	test_reviews, train_reviews = util.get_reviewers(data_path, review_count)
	#util.write_to_file(reviews, 'data/500_plus_reviews.csv')
	w, b = pranking(train_reviews, 0)
	for 

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Run ranking algorithm')
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

  run_pranking(args.path, args.review_count)
