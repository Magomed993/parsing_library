import os
import requests
import sys
import re
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from tululu import get_response, download_file, parse_book_page


def main():
    books_directory = 'books/'
    img_directory = 'image/'
    os.makedirs(books_directory, exist_ok=True)
    os.makedirs(img_directory, exist_ok=True)

    books_content = []

    for number in range(1, 101):
        url = f'https://tululu.org/l55/{number}'
        response = get_response(url)

        soup = BeautifulSoup(response.text, 'lxml')
        books_path = soup.find_all('table', class_='d_book')

        for book in books_path:
            link = book.find('a')['href']
            book_link = urljoin(response.url, link)
            try:
                book_link_response = get_response(book_link)
                book_details = parse_book_page(book_link_response)
                book_soup = BeautifulSoup(book_link_response.text, 'lxml')
                d_book_table = book_soup.find('table', class_='d_book')
                link_txt = d_book_table.find('a', title=f'{book_details['name']} - скачать книгу txt')
                link_img = d_book_table.find('div', class_='bookimage').find('img')['src']
                if link_txt is None:
                    raise requests.exceptions.HTTPError("Ошибочка")
                link_txt_path = link_txt['href']
                download_book_path = urljoin(response.url, link_txt_path)
                download_img_path = urljoin(response.url, link_img)
                book_link_txt_response = get_response(download_book_path)
                book_link_img_response = get_response(download_img_path)
                url_img_parts = urlparse(link_img)
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
                book_content = {
                    'title': book_details['name'],
                    'author': book_details['author'],
                    'img_src': path_txt_parts[0],
                    'comments': book_details['comments'],
                    'genres': book_details['genre']
                }
                books_content.append(book_content)
                # print(book_link)
            except requests.exceptions.HTTPError as error:
                print(f'page - {number}: {error}', file=sys.stderr)
                continue
    book_content_json = json.dumps(books_content)
    with open('book_content.json', 'w') as my_file:
        my_file.write(book_content_json)


if __name__ == '__main__':
    main()
