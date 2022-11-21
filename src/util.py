import csv
import numpy as np
import math

def get_reviewers(ratings_data_path, min_review_count):
	total_reviews = []
	with open(ratings_data_path, newline = '') as csvfile:
		spamreader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
		userId = -math.inf
		review_count = 0
		ratings = []
		for idx, row in enumerate(spamreader):
			
			if idx == 0 and row[0] == 'userId':
				continue

			if userId < int(row[0]):
				userId = int(row[0])
				ratings = []
				review_count = 0

			if userId == int(row[0]):
				review_count += 1
				ratings.append(float(row[2]))

			if review_count == min_review_count:# and idx < 500000:
				ratings = [userId] + ratings
				total_reviews.append(ratings)
				userId += 1
				ratings = []
				review_count = 0
	return split_data(total_reviews, 0.25)

def split_data(data, ratio):
	data = np.array(data)
	userIds = data[:,0]
	data = np.delete(data, 0, 1)
	np.random.shuffle(data)
	test_reviews = data[:, 0:math.floor(len(data.T) * ratio)]
	test_reviews = np.concatenate((np.array([userIds]).T, test_reviews), 1)
	train_reviews = np.delete(data, 0, 1)
	return test_reviews, train_reviews

def write_to_file(data, file_path):
	with open(file_path, 'w', newline='') as f:
		write = csv.writer(f)
		for line in data:
			userId = line.pop(0)
			for rating in line:
				write.writerow([userId, rating])