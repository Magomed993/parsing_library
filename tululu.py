import requests
import os
import argparse
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError("Ошибочка на редиректе")


def download_txt(url, filename, folder='books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = requests.get(url)
    response.raise_for_status()
    format_filename = sanitize_filename(filename)
    directory = f'{folder}{format_filename}.txt'
    check_for_redirect(response)
    with open(directory, 'wb') as file:
        file.write(response.content)
    return directory


def download_image(url, filename, folder='image/'):
    """Функция для скачивания картинок.
        Args:
            url (str): Cсылка на картинки, которые хочется скачать.
            filename (str): Имя файла, с которым сохранять.
            folder (str): Папка, куда сохранять.
        Returns:
            str: Путь до файла, куда сохранёны картинки.
        """
    response = requests.get(url)
    response.raise_for_status()
    format_filename = sanitize_filename(filename)
    directory = f'{folder}{format_filename}'
    check_for_redirect(response)
    with open(directory, 'wb') as file:
        file.write(response.content)
    return directory


def parse_book_page(url):
    """Функция для выявления данных из сайта tululu.org.
        Args:
            url (str): Cсылка на сайт, из которого выявляются данные.
        Returns:
            dict: Данные с сайта: название, автор, ссылка на картинку и т.д.
        """
    book_site = 'https://tululu.org/'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('h1').text.split('::')
    path_img = soup.find('div', class_='bookimage').find('img')['src']
    tag_comments = soup.find_all('div', class_='texts')
    tag_genres = soup.find('span', class_='d_book').find_all('a')
    book_title = title[0].strip()
    author = title[1].strip()
    image_link = urljoin(book_site, path_img)
    comments = []
    for comment in tag_comments:
        comments.append(comment.find('span').text)
    genres = []
    for genre in tag_genres:
        genres.append(genre.text)
    site_data = {
        'name': book_title,
        'author': author,
        'url_image': image_link,
        'comments': comments,
        'genre': genres,
    }
    return site_data


def main():
    books_directory = 'books/'
    img_directory = 'image/'
    os.makedirs(books_directory, exist_ok=True)
    os.makedirs(img_directory, exist_ok=True)
    argument_parse = argparse.ArgumentParser(description="""Скачивает книгу в количестве по значению установленному по умолчанию.
Прописав аргументы даёт возможность установить количество книг необходимое для скачивания (начало цикла - конец цикла).
    """)
    argument_parse.add_argument('start_id', default=1, nargs='?', type=int, help='Начало цикла')
    argument_parse.add_argument('end_id', default=11, nargs='?', type=int, help='Конец цикла')
    args = argument_parse.parse_args()

    for i in range(args.start_id, args.end_id):
        url_txt = f"https://tululu.org/txt.php?id={i}"
        data_url = f'https://tululu.org/b{i}/'
        try:
            data_book = parse_book_page(data_url)
            filename = f"{i}. {data_book['name']} - {data_book['author']}"
            link_parse = urlparse(data_book['url_image'])
            path_separation = os.path.splitext(link_parse.path)
            download_image(data_book['url_image'], f'{i}{path_separation[-1]}', img_directory)
            download_txt(url_txt, filename, books_directory)
            print('Название: ', data_book['name'])
            print('Автор: ', data_book['author'])
            print()
        except requests.exceptions.HTTPError:
            continue

if __name__ == '__main__':
    main()