from requests import get
import json
import os
from bs4 import BeautifulSoup
from urllib.parse import unquote

url_dir = 'scraping/urls'
urls = {}
host = 'http://lib.buet.ac.bd:8080'

for filename in os.listdir(url_dir):
    if filename.endswith('.json'):
        file_path = os.path.join(url_dir, filename)
        with open(file_path, 'r') as f:
            urls[filename.split('.')[0]] = json.load(f)

def fetch_data(url):
    try:
        response = get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.text
    except Exception as e:
        print(f"Error fetching data from {url}: {e}")
        return None
    
def pdf_data(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    pdf_link = soup.find(class_='file-link')
    l = pdf_link
    if pdf_link:
        pdf_link = pdf_link.findChild('a')
        pdf_link = pdf_link.get('href')
    else:
        print("PDF link not found.")
        return None
    print(pdf_link)
    file_name = unquote(pdf_link.split('.pdf')[0].split('/')[-1]) + '.pdf'
    pdf_link = host + pdf_link
    try:
        response = get(pdf_link)
        response.raise_for_status()  # Raise an error for bad responses
        return response.content, file_name
    except Exception as e:
        print(f"Error fetching PDF from {pdf_link}: {e}")
        return None


for dept in urls.keys():
    print(dept)
    os.makedirs('scraping/pdf', exist_ok=True)
    for url in urls[dept]:
        pdf,filename = pdf_data(fetch_data(url))
        with open(f'scraping/pdf/{dept},{filename}.pdf', 'wb') as f:
            f.write(pdf)
            print("PDF saved successfully.")
            f.close()


'''pdf = pdf_data(fetch_data(urls['civil'][0]))




with open('scraping/test.pdf', 'wb') as f:
    f.write(pdf)
    print("PDF saved successfully.")
    f.close()
# Example usage'''