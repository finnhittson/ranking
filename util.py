import csv
import numpy as np

def get_reviewers(ratings_data_path, min_review_count):
	total_reviews = []
	with open(ratings_data_path, newline = '') as csvfile:
		spamreader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
		userId = 1
		review_count = 0
		ratings = []
		for row in spamreader:
			if review_count == min_review_count:
				total_reviews.append(ratings)
				ratings = []
				review_count = 0
				userId += 1
			if userId == int(row[0]):
				review_count += 1
				ratings.append(float(row[2]))
		if review_count == min_review_count:
			total_reviews.append(ratings)
	return np.array(total_reviews).T