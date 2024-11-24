# Парсер книг с сайта [tululu.org](https://tululu.org/)
Скачивание книг с сайта [tululu.org](https://tululu.org/)
## Как установить
Скачайте код с [GitHub](https://github.com/). Python3 должен быть уже установлен. 
Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
## Скрипты и их запуск
### `tululu.py`
```
python3 tululu.py
```
Скрипт выполняет скачивание книг с сайта [tululu.org](https://tululu.org/) в текстовом формате txt, а также их изображение.
### `parse_tululu_category.py`
```
python3 parse_tululu_category.py
```
Скрипт выполняет скачивание книг по страницам с сайта [tululu.org](https://tululu.org/) в текстовом формате txt, а также их изображение.
## Аргументы
### Скрипт `tululu.py`:
```
python3 tululu.py 10 15
```
Данные аргументы позволяют скачивать по страницам. То есть от 10 до 15 страницы скрипт будет скачивать.\
В случае, если аргумент не указан, скачиваться будет по страницам по умолчанию от 1 до 10 включительно.

Не во всех страницах имеется ссылка на скачивание книги и поэтому не все книги по порядку будут скачиваться.
### Скрипт `parse_tululu_category.py`:
- `start_page` - старт скачивания страниц книг;
- `end_page` - конец скачивания книг;
- `--skip_txt` - не скачивать книги в формате txt;
- `--skip_imgs` - не скачивать обложки книг;
- `--dest_folder` - путь к каталогу.

Пример:
```
python3 parse_tululu_category.py 699 701 --skip_imgs
```
Команда произведет скачивание книг от страницы 699 до 701 без скачивания обложек к ним.\
В случае если аргументы не будут указаны, скачивание будет происходить по умолчанию от 1 до 701 включительно.

Не во всех страницах имеется ссылка на скачивание книги и поэтому не все книги по порядку будут скачиваться.
## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).