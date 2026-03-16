import os
import json
import math

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from livereload import Server
from more_itertools import chunked
from urllib.parse import quote


BOOKS_PER_PAGE = 10


def main():
    load_dotenv()
    json_path = os.getenv('DATA_PATH', 'meta_data.json')

    with open(json_path, 'r', encoding='utf-8') as f:
        books = json.load(f)

    total_pages = math.ceil(len(books) / BOOKS_PER_PAGE)
    pages = list(chunked(books, BOOKS_PER_PAGE))

    env = Environment(loader=FileSystemLoader('.'))
    env.filters['urlencode'] = lambda u: quote(u)
    template = env.get_template('template.html')

    output_dir = 'pages'
    os.makedirs(output_dir, exist_ok=True)

    for i, page_books in enumerate(pages, start=1):
        rows = list(chunked(page_books, 2))
        rendered_page = template.render(
            rows=rows,
            current_page=i,
            total_pages=total_pages
        )
        filename = f'index{i}.html'
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(rendered_page)


if __name__ == '__main__':
    main()

    server = Server()
    server.watch('template.html', main)
    server.watch('render_website.py', main)
    server.watch('eta_data.json', main)
    server.serve(root='.', default_filename='index.html')
