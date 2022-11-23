import argparse
import util
import math
import random
import numpy as np
import copy

def pranking(reviews, cycles):
	reviews = np.array(reviews)
	w = np.array([0] * (len(reviews) - 1))
	b = [0] * 10
	len_b = len(b)

	for _ in range(cycles):
		random_viewer = int(random.uniform(0,len(reviews.T)))
		np.random.shuffle(reviews)
		target_rank = copy.copy(reviews[random_viewer, :]) * 2
		#reviews[random_viewer, :] = np.zeros(len(target_rank))
		reviews = np.delete(reviews,random_viewer,0)

		for idx, review_set in enumerate(reviews.T):
			w_dot_x = w.dot(review_set)
			predicted_rank = predict_rank(w_dot_x, b)
			if target_rank[idx] != predicted_rank / 2:
				
				correction_vect = []
				for r in range(len_b):
					if target_rank[idx] - 2.5 <= r:
						correction_vect.append(-1)
					else:
						correction_vect.append(1)

				tau = []
				for r in range(len_b):
					if (w_dot_x - b[r]) * correction_vect[r] <= 0: # incorrect
						tau.append(correction_vect[r])
					else: # correct
						tau.append(0)
				if idx < 3 and False:
					print(tau)
					print(w)
					print(w_dot_x)
					print()
					
				w = w + sum(tau) * review_set
				for r in range(len_b):
					b[r] = b[r] - tau[r]

		reviews = np.concatenate((reviews, np.array([target_rank])), axis=0)
		#reviews[random_viewer,:] = target_rank
	
	return w, b

def predict_rank(w_dot_x, b):
	yt_hat = math.inf
	r = 0
	while r < len(b):
		if w_dot_x - b[r] < 0 and r < yt_hat:
			yt_hat = r
		r += 1
	return yt_hat

def run_pranking(data_path, review_count):
	_, train_reviews = util.get_reviewers(data_path, review_count)
	#util.write_to_file(test_reviews, 'data/100_quick.csv')
	w, b = pranking(train_reviews,500)
	print(w,b)
	correct_count = 0
	random_viewer = int(random.uniform(0,len(train_reviews)))
	true_ranks = copy.copy(train_reviews[random_viewer, :])
	#train_reviews[random_viewer, :] = np.zeros(len(true_ranks))
	train_reviews = np.delete(train_reviews, random_viewer, 0)

	for idx, review in enumerate(train_reviews.T):			
		predicted_rank = predict_rank(w.dot(review), b)
		if idx%10 == 0 and not False:
			print(round(w.dot(review), 2))
			#print("true_rank: {}".format(true_ranks[idx]))
			#print("predicted_rank: {}".format(predicted_rank/2))
			#print(predicted_rank / 2 == true_ranks[idx])
			#print()
		if predicted_rank / 2 == true_ranks[idx]:
			correct_count += 1
	print("\n {}%".format(correct_count))

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
