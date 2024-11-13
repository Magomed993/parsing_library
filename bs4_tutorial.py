import requests
from bs4 import BeautifulSoup


url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('main').find('header').find('h1').text
img_tag = soup.find('img', class_='attachment-post-image')['src']
text_tag = soup.find('main').find('div', class_='entry-content').find('p').text
print(f'{title_tag}\n{img_tag}\n\n{text_tag}')
