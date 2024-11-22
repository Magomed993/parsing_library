import os
import requests
import sys
import re
import json
import argparse
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tululu import get_response, download_file, parse_book_page


def main():
    books_directory = 'books/'
    img_directory = 'image/'
    os.makedirs(books_directory, exist_ok=True)
    os.makedirs(img_directory, exist_ok=True)

    books_content = []
    argument_parse = argparse.ArgumentParser(description="""Скачивает книги по страницам установленным по умолчанию.
    Прописав аргументы даёт возможность установить диапазон страниц необходимое для скачивания книг (начало цикла - конец цикла).
        """)
    argument_parse.add_argument('start_page', default=1, nargs='?', type=int, help='Начало цикла')
    argument_parse.add_argument('end_page', default=701, nargs='?', type=int, help='Конец цикла')
    args = argument_parse.parse_args()
    for number in range(args.start_page, args.end_page):
        url = f'https://tululu.org/l55/{number}'
        response = get_response(url)

        soup = BeautifulSoup(response.text, 'lxml')
        d_book_selector = 'table.d_book'
        # books_path = soup.find_all('table', class_='d_book')
        books_path = soup.select(d_book_selector)
        for book in books_path:
            link = book.select_one('a')['href']
            book_link = urljoin(response.url, link)

            book_link_response = get_response(book_link)
            book_details = parse_book_page(book_link_response)
            book_soup = BeautifulSoup(book_link_response.text, 'lxml')
            d_book_table = book_soup.select_one(d_book_selector)
            txt_link_selector = f'a[title="{book_details['name']} - скачать книгу txt"]'
            try:
                # txt_link = d_book_table.find('a', title=f'{book_details['name']} - скачать книгу txt')
                txt_link = d_book_table.select_one(txt_link_selector)
                img_link_selector = 'div.bookimage img'
                # img_link = d_book_table.find('div', class_='bookimage').find('img')['src']
                img_link = d_book_table.select_one(img_link_selector)['src']
                if txt_link is None:
                    raise requests.exceptions.HTTPError("Невозможно скачать, контент недоступен")
                link_txt_path = txt_link['href']
                download_book_path = urljoin(response.url, link_txt_path)
                download_img_path = urljoin(response.url, img_link)
                book_link_txt_response = get_response(download_book_path)
                book_link_img_response = get_response(download_img_path)
                url_img_parts = urlparse(img_link)
                url_txt_parts = urlparse(link_txt_path)
                path_img_parts = os.path.splitext(url_img_parts.path)
                path_txt_parts = os.path.splitext(url_txt_parts.query)
                # print(path_img_parts)
                book_img_str_number = re.findall(r'\d+', path_img_parts[0])
                book_txt_number = int(re.findall(r'\d+', path_txt_parts[0])[0])
                if book_img_str_number:
                    book_img_number = int(book_img_str_number[0])
                else:
                    book_img_number = f'nopic'
                # print(book_img_str_number)
                file_name = f'{book_txt_number}: {book_details['name']} - {book_details['author']}.txt'
                download_file(book_link_txt_response, file_name, books_directory)
                download_file(book_link_img_response, f'{book_img_number}{path_img_parts[-1]}', img_directory)
                # book_txt_path = urlparse(book_link_txt_response)
                book_content = {
                    'title': book_details['name'],
                    'author': book_details['author'],
                    'img_src': f'{img_directory}{book_img_number}{path_img_parts[-1]}',
                    'book_path': f'{books_directory}{book_details['name']}.txt',
                    'comments': book_details['comments'],
                    'genres': book_details['genre']
                }
                books_content.append(book_content)
                print(book_link_response.url)
            except requests.exceptions.HTTPError as error:
                print(f'{book_link_response.url}: {error}', file=sys.stderr)
                continue
    book_content_json = json.dumps(books_content)
    with open('book_content.json', 'w') as my_file:
        my_file.write(book_content_json)


if __name__ == '__main__':
    main()
