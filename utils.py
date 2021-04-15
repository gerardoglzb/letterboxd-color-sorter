import random
import colorsys
from PIL import Image
from collections import namedtuple
from math import sqrt


Point = namedtuple('Point', ('count', 'pixel'))
Cluster = namedtuple('Cluster', ('points', 'center'))


def euclidean_distance(point1, point2):
	return sqrt(sum([(point1.pixel[i] - point2.pixel[i]) ** 2 for i in range(3)]))


def get_most_dominant(clusters):
	largest_count = 0
	for idx, cluster in enumerate(clusters):
		if len(cluster.points) > largest_count:
			largest_count = len(cluster.points)
			largest_idx = idx
	return list(map(int, clusters[largest_idx].center.pixel))


def get_center(points):
	counts_sum = 0
	values = [0.0 for i in range(3)]
	for point in points:
		counts_sum += point.count
		for i in range(3):
			values[i] += (point.pixel[i] * point.count)
	return Point(1, [(val / counts_sum) for val in values])


def get_points(img):
	points = []
	width, height = img.size
	for count, pixel in img.getcolors(width * height):
		points.append(Point(count, pixel))
	return points


def k_means_clustering(points):
	clusters = [Cluster([point], point) for point in random.sample(points, 3)]
	loop = True
	while loop:
		point_lists = [[] for i in range(3)]
		for point in points:
			smallest_distance = float('inf')
			for i in range(3):
				distance = euclidean_distance(point, clusters[i].center)
				if distance < smallest_distance:
					smallest_distance = distance
					smallest_idx = i
			point_lists[smallest_idx].append(point)

		difference = 0
		for i in range(3):
			prev = clusters[i]
			center = get_center(point_lists[i])
			clusters[i] = Cluster(point_lists[i], center)
			difference = max(difference, euclidean_distance(prev.center, clusters[i].center))

		if difference < 1:
			loop = False

	return clusters


def get_dominant_color(img):
	# img.thumbnail((100, 100)) # optional
	width, height = img.size
	points = get_points(img)
	clusters = k_means_clustering(points)
	return get_most_dominant(clusters)


def step(r, g, b, repetitions=1):
	lum = sqrt(.241 * r + .691 * g + .068 * b)
	h, s, v = colorsys.rgb_to_hsv(r, g, b)
	h_rep = int(h * repetitions)
	v_rep = int(v * repetitions)

	if h_rep % 2 == 1:
		v_rep = repetitions - v_rep
		lum = repetitions - lum

	return (h_rep, lum, v_rep)
