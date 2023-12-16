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

# Functions for scraping, counting URLs, and categorizing

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
