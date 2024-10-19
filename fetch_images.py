# fetch_images.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def fetch_traffic_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags that may contain traffic camera images
    images = soup.find_all('img')
    image_urls = []

    for img in images:
        img_url = img.get('src')
        if img_url and 'traffic' in img_url:  # Adjust this condition as needed
            # Ensure the URL is complete
            full_url = urljoin(url, img_url)  # Join the base URL with the relative URL
            image_urls.append(full_url)

    return image_urls

def download_image(image_url):
    response = requests.get(image_url)
    if response.status_code == 200:
        file_name = image_url.split("/")[-1]
        with open(file_name, 'wb') as f:
            f.write(response.content)
        return file_name
    else:
        return None
