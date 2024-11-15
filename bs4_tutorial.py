import requests
from bs4 import BeautifulSoup


url = 'https://www.franksonnenbergonline.com/blog/are-you-grateful/'
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'lxml')
tag_title = soup.find('main').find('header').find('h1').text
tag_img = soup.find('img', class_='attachment-post-image')['src']
tag_text = soup.find('main').find('div', class_='entry-content').find('p').text
print(f'{tag_title}\n{tag_img}\n\n{tag_text}')
