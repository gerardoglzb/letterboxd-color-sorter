import requests
import colorsys
import math
import csv
import re
from PIL import Image
from bs4 import BeautifulSoup
from rgb_calculator import calculate_rgb, step

def get_film_slug(title):
	return "-".join(re.split("' |: |, |; | & | + | |'|:|\.|,|;|\?|!|\(|\)|&|@|#|\[|\]|/|\$|\+|=|-|\*|\{|\}", title)).lower()


def get_soup(url):
	source = requests.get(url).text
	soup = BeautifulSoup(source, 'lxml')
	return soup


def get_img_url(soup):
	return soup.find('div', {'data-component-class': 'globals.comps.FilmPosterComponent'}).find('img')['src']


def get_year(soup):
	return soup.find('div', {'data-component-class': 'globals.comps.FilmPosterComponent'})['data-film-release-year']


class FilmData:
	def __init__(self, title, year):
		self.title = title
		self.year = year
		self._img = None
		self.rgb = None

	@property
	def img(self):
		return self._img

	@img.setter
	def img(self, val):
		self._img = val
		self.rgb = calculate_rgb(self._img)

	@img.deleter
	def img(self):
		del self._img
	

url = ""
output_name = ""
soup = get_soup(url)

posters = soup.find_all('div', class_="poster film-poster really-lazy-load")

all_data = []
x = 1
for poster in posters:
	print("poster", x)
	x += 1
	title = poster.find('img')['alt']
	film_url = f"https://letterboxd.com{poster['data-target-link']}"
	film_soup = get_soup(film_url)
	img_url = get_img_url(film_soup)
	year = get_year(film_soup)
	film_data = FilmData(title, year)
	try:
		img = Image.open(requests.get(img_url, stream=True).raw)
		film_data.img = img
		all_data.append(film_data)
	except:
		print(f"{title} img fail")

all_data.sort(key=lambda data: step(data.rgb[0], data.rgb[1], data.rgb[2], 8))

with open(f"{output_name}.csv", 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow(["Title", "Year"])
	for data in all_data:
		writer.writerow([data.title, data.year])
