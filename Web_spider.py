import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys
import os


def banner():
    print("\n\n")
    print("""
        
 /$$      /$$           /$$              /$$$$$$            /$$       /$$                    
| $$  /$ | $$          | $$             /$$__  $$          |__/      | $$                    
| $$ /$$$| $$  /$$$$$$ | $$$$$$$       | $$  \__/  /$$$$$$  /$$  /$$$$$$$  /$$$$$$   /$$$$$$ 
| $$/$$ $$ $$ /$$__  $$| $$__  $$      |  $$$$$$  /$$__  $$| $$ /$$__  $$ /$$__  $$ /$$__  $$
| $$$$_  $$$$| $$$$$$$$| $$  \ $$       \____  $$| $$  \ $$| $$| $$  | $$| $$$$$$$$| $$  \__/
| $$$/ \  $$$| $$_____/| $$  | $$       /$$  \ $$| $$  | $$| $$| $$  | $$| $$_____/| $$      
| $$/   \  $$|  $$$$$$$| $$$$$$$/      |  $$$$$$/| $$$$$$$/| $$|  $$$$$$$|  $$$$$$$| $$      
|__/     \__/ \_______/|_______/        \______/ | $$____/ |__/ \_______/ \_______/|__/      
                                                 | $$                                        
                                                 | $$                                        
                                                 |__/                                        

   *════════════════════════════════════════════════════════════════*
      ╔════════════════════════════════════════════════════════════╗
      ║     By        : Koushal Kedari                              ║                                                                        
      ║     Github    : https://github.com/Nightowl-code           ║
      ║     Licence   : MIT                                        ║
      ║     Code      : Python                                     ║ 
      ╚════════════════════════════════════════════════════════════╝
    *════════════════════════════════════════════════════════════════*

          
          
           """)
    print("\n")




visited_links = set()

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    return links

def scrape_url(url, depth, output_file):
    global visited_links

    if depth == 0 or url in visited_links:
        return

    visited_links.add(url)
    with open(output_file, 'a') as file:
        file.write(f"{url}\n")

    links = get_links(url)

    if depth > 1:
        for link in links:
            scrape_url(link, depth - 1, output_file)

def count_urls_in_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
            return len(content)
    except FileNotFoundError:
        return 0

def categorize_urls(output_file):
    try:
        extensions = {}
        with open(output_file, 'r') as file:
            for line in file:
                line = line.strip()
                extension = os.path.splitext(line)[1][1:]
                if extension not in extensions:
                    extensions[extension] = []
                extensions[extension].append(line)
        
        # Write categorized URLs to the file
        with open(output_file, 'a') as file:
            file.write("\nCategorized URLs:\n")
            for ext, urls in extensions.items():
                file.write(f"\n{ext.upper()}:\n")
                for url in urls:
                    file.write(f"{url}\n")
    except FileNotFoundError:
        print("Output file not found.")



        

def main():
    banner()

    while True:
        start_url = input("Enter the target URL: ")
        recursion_depth = int(input("Enter recursion depth: "))
        output_file = input("Enter output file path: ")






        try:
            scrape_url(start_url, recursion_depth, output_file)
            print("Scraping completed successfully.")
        except KeyboardInterrupt:
            with open(output_file, 'a') as file:
                file.write("\nAborted by user.")
                
                urls_count = count_urls_in_file(output_file)
                file.write(f"\nNumber of URLs found: {urls_count}\n")
                
                print(f"Number of URLs found: {urls_count}")
                print(f"Number of URLs in file: {urls_count}")

                categorize_urls(output_file)  # Categorizing URLs after printing counts

            sys.exit(0)

        choice = input("Do you want to scrape another URL? (Y/N): ").strip().lower()
        if choice != 'y':
            break

if __name__ == '__main__':
    main()
