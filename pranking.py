import argparse
import util
import math
import random
import numpy as np

b = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]

def pranking(reviews):
	
	random_viewer = 2#int(random.uniform(0,len(reviews.T)))
	yt = reviews[:,random_viewer]
	reviews = np.delete(reviews,random_viewer,1)
	
	w = np.array([0] * len(reviews.T))
	b = [0] * 10
	len_b = len(b)

	for idx, review in enumerate(reviews):
				
		yt_hat = predict(w, b, review)
		if yt[idx] != yt_hat:
			
			w_correction = []
			for r in range(len_b):
				if yt[idx] <= b[r]:
					w_correction.append(-1)
				else:
					w_correction.append(1)

			tau = []
			for s in range(len_b):
				if (w_dot_x - b[s]) * w_correction[s] <= 0: # incorrect prediction
					tau.append(w_correction[s])
				else: # correct prediction
					tau.append(0)

			w = w + sum(tau) * review
			for t in range(len_b):
				b[t] = b[t] - tau[t]

	return w, b

def predict_rank(w, b, x):

	yt_hat = math.inf
	w_dot_x = w.dot(x)
	rank_idx = 0
	while rank_idx < len(b):
		if w_dot_x - b[rank_idx] < 0 and rank_idx < yt_hat:
			yt_hat = rank_idx
			rank_idx = len(b) + 1
		rank_idx += 1
	return yt_hat

def run_pranking(data_path, review_count):
	reviews = util.get_reviewers(data_path, review_count)
	w, b = pranking(reviews)
	print(w,b)

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

  pranking(args.path, args.review_count)
