import csv
import numpy as np
import math
import re
import copy
import random

def get_reviews(ratings_data_path):
	total_reviews = []
	with open(ratings_data_path, newline = '') as csvfile:
		spamreader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
		userId = -math.inf
		reviews = []
		for idx, row in enumerate(spamreader):
			if idx == 0 and row[0] == 'userId':
				continue

			if userId != int(row[0]):
				if len(reviews) != 0:
					total_reviews.append(reviews)
				userId = int(row[0])
				reviews = []

			if userId == int(row[0]):
				reviews.append(float(row[2]))
	return total_reviews


def get_n_reviews(ratings_data_path, review_count):
	total_reviews = []
	
	with open(ratings_data_path, newline = '') as csvfile:
		spamreader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
		userId = -math.inf
		reviews = []
		
		for idx, row in enumerate(spamreader):
			
			if idx == 0 and row[0] == 'userId':
				continue

			if len(reviews) == review_count:
				total_reviews.append(reviews)
				reviews = []
				userId += 1

			if userId < int(row[0]):
				userId = int(row[0])
				reviews = []

			if userId == int(row[0]):
				reviews.append(float(row[2]))
		if len(reviews) == review_count:
			total_reviews.append(reviews)

	return total_reviews


def get_all_reviewers(ratings_data_path, min_movie_count):
	total_reviews = []
	with open(ratings_data_path, newline = '') as csvfile:
		spamreader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
		userId = -math.inf
		review_count = 0
		reviews = []
		movieIds = []
		data_indices = []
		userId_list = []
		#min_movie_count = 5
		for idx, row in enumerate(spamreader):
			if idx == 0 and row[0] == 'userId':
				continue

			if userId < int(row[0]):
				if len(movieIds) != 0:
					total_reviews.append([movieIds, reviews])
					data_indices = append_sort(data_indices, review_count, userId)
					userId_list.append(userId)
				userId = int(row[0])
				reviews = []
				movieIds = []
				review_count = 0

			if userId == int(row[0]):
				review_count += 1
				reviews.append(float(row[2]))
				movieIds.append(int(row[1]))

		if len(movieIds) != 0:
			total_reviews.append([movieIds, reviews])
			data_indices = append_sort(data_indices, review_count, userId)
			userId_list.append(userId)

		matched_reviewers, reviews_idx = find_common_movies(data_indices, total_reviews, min_movie_count)
		print(matched_reviewers)
		file_path = 'data/new_100_plus_reviews.csv'
		write_common_users(matched_reviewers, reviews_idx, total_reviews, file_path, userId_list)
	return 0


def write_common_users(matched_reviewers, reviews_idx, total_reviews, file_path, userId_list):
	with open(file_path, 'w', newline='') as f:
		write = csv.writer(f)
		write.writerow(["userId", "movieId", "rating"])
		for userId in matched_reviewers:
			userId_reviews = sparsify(total_reviews[userId - 1][0], total_reviews[userId - 1][1]) 
			for review_idx in reviews_idx:
				write.writerow([userId, review_idx, userId_reviews[review_idx]])


def find_common_movies(data_indices, total_reviews, min_movie_count):
	master_list = total_reviews[data_indices[0][0] - 1]
	master_list = sparsify(master_list[0], master_list[1])
	matched_reviewers = []
	for idx, data_index in enumerate(data_indices):
		comp_list = total_reviews[data_index[0] - 1]
		comp_list = sparsify(comp_list[0], comp_list[1])
		overlaps = overlap(master_list, comp_list)
		if overlaps >= min_movie_count:
			matched_reviewers.append(data_index[0])
		for i in range(len(master_list)):
			if not illogical_and(master_list[i], comp_list[i]) and overlaps >= min_movie_count:
				master_list[i] = 0
	return matched_reviewers, [i for i, e in enumerate(master_list) if e != 0]


def overlap(list1, list2):
	if len(list1) != len(list2):
		return None
	overlap = 0
	for i in range(len(list1)):
		if list1[i] != 0 and list2[i] != 0:
			overlap += 1
	return overlap


def get_common_users(master_list, total_reviews):
	for pair in master:
		print("HERE")


def sparsify(movieIds, reviews):
	movie_count = 62000
	#movie_count = 20
	if len(movieIds) != len(reviews):
		return None
	sparse_bitch = []
	movie_idx = 0
	for i in range(movie_count):
		if movie_idx < len(movieIds) and movieIds[movie_idx] == i:
			sparse_bitch.append(reviews[movie_idx])
			movie_idx += 1
		else: sparse_bitch.append(0)
	return sparse_bitch


def illogical_and(a,b):
	if a != 0 and b != 0:
		return True
	return False


def review_sum(review_list):
	i = 0
	for review in review_list:
		if review != 0:
			i += 1
	return i


def append_sort(all_data_indices, add_me_sum, idx):
	if len(all_data_indices) == 0:
		return [[idx, add_me_sum]]
	for jdx, pair in enumerate(all_data_indices):
			if pair[1] < add_me_sum:
				all_data_indices.insert(jdx, [idx, add_me_sum])
				return all_data_indices
	all_data_indices.append([idx, add_me_sum])
	return all_data_indices


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
				write.writerow([idx, "",rating])


def get_queries(data_path):
	X = []
	y = []
	with open(data_path, newline = '') as csvfile:
		spamreader = csv.reader(csvfile, delimiter = ' ', quotechar = '|')
		for idx, query in enumerate(spamreader):
			x_i = []
			for jdx, element in enumerate(query):
				if jdx == 0:
					y.append(int(element))
				elif jdx > 1 and jdx < 27:
					x_i.append(float(re.sub(r'^.*?:', '', element)))
			X.append(x_i)
	return X, y


def split_queries(X, y, ratio):
	tmp = list(zip(X,y))
	#random.shuffle(tmp)
	X, y = zip(*tmp)
	X_test = X[:math.floor(len(X) * ratio)]
	X_train = X[math.floor(len(X) * ratio):]
	y_test = y[:math.floor(len(y) * ratio)]
	y_train = y[math.floor(len(y) * ratio):]
	return list(X_train), list(y_train), list(X_test), list(y_test)


def make_data(reviewers, movies_watched):
	data = []
	for reviwer in range(reviewers):
		reviews = []
		for movie in range(movies_watched):
			reviews.append(int(random.uniform(1,11)) / 2)
		data.append(reviews)
	write_to_file(data, 'data/toy_data.csv')