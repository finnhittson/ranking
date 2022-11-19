import argparse
import util
import math
import random

def pranking(data_path, review_count):
	reviews = util.get_reviewers(data_path, review_count)
	
	w = [0] * len(reviews)
	b = [0] * 10
	bk = float('inf')
	y_t = reviews.pop(int(len(reviews) * random.uniform(0,1)))
	print(y_t)
	for review in reviews:
		print(review)

	


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
