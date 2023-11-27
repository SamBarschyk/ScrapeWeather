import requests
from bs4 import BeautifulSoup
import os

def get_cache_filename(url):
    return f"cache/{url.replace('/', '_').replace(':', '_').replace('.', '_')}.html"

def download_url(url):
    if not os.path.exists('cache'):
        os.makedirs('cache')
    cache_filename = get_cache_filename(url)
    if os.path.exists(cache_filename):
        with open(cache_filename, 'r', encoding='utf-8') as file:
            content = file.read()
        print("Using cached content.")
        return content
    response = requests.get(url)
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        with open(cache_filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print("Downloaded and cached content.")
        return content
    else:
        print(f"Failed to download the page. Status code: {response.status_code}")
        return None
if __name__ == '__main__':
    url = "https://ua.sinoptik.ua/погода-дрогобич"
    content = download_url(url)
    if content is None:
        print("ERROR: CONTENT_IS_NONE")
        exit()
    soup = BeautifulSoup(content, 'html.parser')
    main_content_block_elements = soup.select('#mainContentBlock .main')
    if main_content_block_elements:
        for day_index, day_element in enumerate(main_content_block_elements, start=1):
            temperature_element = day_element.find('div', class_='temperature')
            if temperature_element:
                temperature = temperature_element.text.strip()
                description_selector = f'bd{(day_index)}c > div.wDescription.clearfix > div.rSide > div'
                description_element = day_element.select_one(description_selector)
                description = description_element.text.strip() if description_element else 'Опис недоступний'
                print(f"Day {day_index} - Temperature: {temperature}, Description: {description}")
                print("-" * 50)
            else:
                print(f"ERROR: Temperature element not found for day {day_index}")
    else:
        print("ERROR: Day and temperature elements not found on the page.")
