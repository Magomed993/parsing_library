import requests
import os
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse, urlsplit, unquote


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
    response = requests.get(url)
    response.raise_for_status()
    format_filename = sanitize_filename(filename)
    directory = f'{folder}{format_filename}'
    check_for_redirect(response)
    with open(directory, 'wb') as file:
        file.write(response.content)
    return directory


def main():
    directory_books = 'books/'
    directory_img = 'image/'
    os.makedirs(directory_books, exist_ok=True)
    os.makedirs(directory_img, exist_ok=True)
    book_site = 'https://tululu.org/'

    for i in range(1, 11):
        url_download = f"https://tululu.org/txt.php?id={i}"
        url_book = f'https://tululu.org/b{i}/'

        try:
            response = requests.get(url_book)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, 'lxml')
            tag = soup.find('h1').text.split('::')
            img = soup.find('div', class_='bookimage').find('img')['src']
            title = tag[0].strip()
            author = tag[1].strip()
            filename = f"{i}. {title} - {author}"
            site_integration = urljoin(book_site, img)
            link_parse = urlparse(site_integration)
            path_separation = os.path.splitext(link_parse.path)
            download_image(site_integration, f'{i}{path_separation[-1]}', directory_img)
            download_txt(url_download, filename, directory_books)
            # print(f'Заголовок: {title}')
            # print(urljoin(book_site, img))
            # print()
        except requests.exceptions.HTTPError as http_error:
            print(f'Ошибка на ID {i}: {http_error}')
            continue

if __name__ == '__main__':
    main()