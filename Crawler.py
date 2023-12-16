import requests
from bs4 import BeautifulSoup
import concurrent.futures
import argparse
from urllib.parse import urljoin
import threading
import sys

visited_links = set()
visited_links_lock = threading.Lock()

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    return links

def scrape_url(url, depth, output_file):
    global visited_links

    if depth == 0 or url in visited_links:
        return

    print(f"Crawling {url}")

    visited_links.add(url)
    with visited_links_lock:
        with open(output_file, 'a') as file:
            file.write(url + '\n')

    links = get_links(url)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(scrape_url, link, depth - 1, output_file): link for link in links}

        for future in concurrent.futures.as_completed(future_to_url):
            link = future_to_url[future]
            try:
                future.result()
            except Exception as exc:
                print(f"Error Crawling {link}: {exc}")

    # Exit if Ctrl+C is pressed
    if threading.current_thread() is threading.main_thread():
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='Web scraper with multithreading and recursion')
    parser.add_argument('-u', '--url', type=str, help='Target URL', required=True)
    parser.add_argument('-R', '--recursion', type=int, help='Recursion depth', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file path', required=True)
    args = parser.parse_args()

    start_url = args.url
    recursion_depth = args.recursion
    output_file = args.output

    try:
        scrape_url(start_url, recursion_depth, output_file)
    except KeyboardInterrupt:
        print("\nAborted by user.")
        sys.exit(0)

if __name__ == '__main__':
    main()
