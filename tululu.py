import requests
import os
import argparse
import sys
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError("Ошибочка на редиректе")


def download_txt(url, filename, folder='books/'):
    format_filename = sanitize_filename(filename)
    path = f'{folder}{format_filename}.txt'
    with open(path, 'wb') as file:
        file.write(url.content)
    return path


def download_image(url, filename, folder='image/'):
    format_filename = sanitize_filename(filename)
    path = f'{folder}{format_filename}'
    with open(path, 'wb') as file:
        file.write(url.content)
    return path


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    title = soup.find('h1').text.split('::')
    img_path = soup.find('div', class_='bookimage').find('img')['src']
    tag_comments = soup.find_all('div', class_='texts')
    tag_genres = soup.find('span', class_='d_book').find_all('a')
    book_title = title[0].strip()
    author = title[1].strip()
    image_link = urljoin(response.url, img_path)
    comments = [comment.find('span').text for comment in tag_comments]
    genres = [genre.text for genre in tag_genres]
    book_details = {
        'name': book_title,
        'author': author,
        'url_image': image_link,
        'comments': comments,
        'genre': genres,
    }
    return book_details


def get_response(url, params=None):
    response = requests.get(url, params)
    response.raise_for_status()
    check_for_redirect(response)
    return response


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

    for number in range(args.start_id, args.end_id):
        url_txt = f"https://tululu.org/txt.php"
        payload_url_txt = {
            'id': number,
        }
        url_book = f'https://tululu.org/b{number}/'
        try:
            response_book_txt = get_response(url_txt, payload_url_txt)
            response_book_url = get_response(url_book)
            book_details = parse_book_page(response_book_url)
            response_url_image = get_response(book_details['url_image'])
            filename = f"{number}. {book_details['name']} - {book_details['author']}"
            url_parts = urlparse(book_details['url_image'])
            path_parts = os.path.splitext(url_parts.path)
            download_image(response_url_image, f'{number}{path_parts[-1]}', img_directory)
            download_txt(response_book_txt, filename, books_directory)
            print('Название: ', book_details['name'])
            print('Автор: ', book_details['author'])
            print()
        except requests.exceptions.ConnectionError:
            print('Соединение прервано. Скрипт продолжает работу', file=sys.stderr)
        except requests.exceptions.HTTPError as error:
            print(f'id книги - {number}: {error}', file=sys.stderr)
            continue


if __name__ == '__main__':
    main()
