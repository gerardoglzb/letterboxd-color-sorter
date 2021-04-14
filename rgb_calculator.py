import operator

def calculate_rgb(img):
	size = img.size

	rgbs = {}
	for i in range(size[0]):
		for j in range(size[1]):
			pixel = img.getpixel((i, j))
			rgbs[pixel] = rgbs.get(pixel, 0) + 1

	return max(rgbs.items(), key=operator.itemgetter(1))[0]


def step(r, g, b, repetitions=1):
	lum = math.sqrt(.241 * r + .691 * g + .068 * b)
	h, s, v = colorsys.rgb_to_hsv(r, g, b)
	h2 = int(h * repetitions)
	lum2 = int(lum * repetitions)
	v2 = int(v * repetitions)

	if h2 % 2 == 1:
		v2 = repetitions - v2
		lum = repetitions - lum

	return (h2, lum, v2)