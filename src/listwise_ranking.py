import argparse
import util

def listwise_ranking(quieries_data_path):
	util.get_queries(quieries_data_path)


def run_listwise_ranking(data_path):
	util.get_queries(data_path)


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Run listwise ranking algorithm')
	parser.add_argument(
		'path',
		metavar='PATH',
		type=str,
		help='Path to the data.')
	args = parser.parse_args()
	listwise_ranking(args.path)