import logging
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import argparse

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)

class Crawler:
    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls
        self.file_path = r'C:\Users\DELL\OneDrive\Documents\web-crawler\Output.txt'  # File to store fetched URLs

    def download_url(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return response.text
        except requests.RequestException as e:
            logging.error(f"Failed to download {url}: {e}")
            return None

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        urls = []
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            urls.append(path)
        return urls

    def categorize_url(self, url):
        parsed_url = urlparse(url)
        path = parsed_url.path
        if path.endswith(('.jpg', '.jpeg')):
            return 'jpg/jpeg'
        elif path.endswith('.pdf'):
            return 'pdf'
        elif path.endswith('.html'):
            return 'html'
        elif path.endswith('.css'):
            return 'css'
        elif path.endswith('.js'):
            return 'js'
        else:
            return 'other'

    def add_url_to_visit(self, url):
        if url and url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        if html:
            linked_urls = self.get_linked_urls(url, html)
            for link_url in linked_urls:
                self.add_url_to_visit(link_url)
            return linked_urls

    def run(self):
        with open(self.file_path, 'a') as file:
            while self.urls_to_visit:
                url = self.urls_to_visit.pop(0)
                logging.info(f'Crawling: {url}')
                try:
                    linked_urls = self.crawl(url)
                    if linked_urls:
                        for link_url in linked_urls:
                            if link_url:
                                category = self.categorize_url(link_url)
                                file.write(f"{category.upper()} URL: {link_url}\n")
                except Exception as e:
                    logging.exception(f'Failed to crawl {url}: {e}')
                finally:
                    self.visited_urls.append(url)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Web Crawler')
    parser.add_argument('-u', '--url', help='URL to crawl', required=True)
    args = parser.parse_args()

    url_to_crawl = args.url
    Crawler(urls=[url_to_crawl]).run()