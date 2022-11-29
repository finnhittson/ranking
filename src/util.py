import csv
import numpy as np
import math
import re

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
				ratings.append(float(row[1]))

			if review_count == min_review_count:# and len(total_reviews) <= 7542:
				#ratings = [userId] + ratings
				total_reviews.append(ratings)
				userId += 1
				ratings = []
				review_count = 0
			if len(total_reviews) > 7542 and False:
				break
	return split_data(total_reviews, 0)

def split_data(data, ratio):
	data = np.array(data)
	np.random.shuffle(data)
	test_reviews = data[:, 0:math.floor(len(data.T) * ratio)]
	train_reviews = data[:, math.floor(len(data.T) * ratio):]
	return test_reviews, train_reviews

def write_to_file(data, file_path):
	with open(file_path, 'w', newline='') as f:
		write = csv.writer(f)
		for idx, line in enumerate(data):
			for rating in line:
				write.writerow([idx, rating])

def get_queries(data_path):
	x = []
	with open(data_path, newline = '') as csvfile:
		spamreader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
		for idx, query in enumerate(spamreader):
			x_i = []
			for jdx, element in enumerate(query):
				if jdx == 0:
					x_i.append(element)
				elif jdx > 1 and jdx < 27:
					x_i.append(re.sub(r'^.*?:', '', element))
			x.append(x_i)