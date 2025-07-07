import json
import uuid

import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from utils_scraper import format_price


class ProductScraper:
    def __init__(self, pathname):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.pathname = pathname

        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--window-size=1920x1080')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-extensions')

    def scrape_product_detaiil(self, brand):
        print("Scraping :" + self.pathname)
        req = requests.get(self.pathname, headers=self.headers)
        soup = BeautifulSoup(req.content, 'lxml')

        name_product = soup.find('h1', class_='js-product-name').text.strip()
        try:
            price_product_str = soup.find('div', class_='js-price-display').text.strip()
        except AttributeError:
            price_product_str = soup.find('h3', class_='js-price-display').text.strip()

        try:
            desc_product = soup.find('div', class_='user-content font-small mb-4').text.strip()
        except AttributeError:
            try:
                desc_product = soup.find('div', class_='product-description').text.strip()
            except AttributeError:
                desc_product =''


        try:
            sizes_seletor_tag = soup.find('select', id='variation_2')
            sizes_options_tag = sizes_seletor_tag.find_all('option')
            sizes = set()
            for option in sizes_options_tag:
                size = option.text.strip()
                sizes.add(size)
        except AttributeError:
            sizes = set()

        try:
            colors_seletor_tag = soup.find('select', id='variation_1')
            colors_options_tag = colors_seletor_tag.find_all('option')
            colors = set()
            for option in colors_options_tag:
                color = option.text.strip()
                colors.add(color)
        except AttributeError:
            colors = set()


        try:
            img_product = soup.find_all('div', class_='js-product-slide')
        except AttributeError:
            img_product = soup.find_all('div', class_='swiper-slide')


        imgs = set()
        for img in img_product:
            link = img.find('a')
            if link and link.get('href'):
                imgs.add(link.get('href'))

        return {
            'id': str(uuid.uuid4()),
            'name': name_product,
            'price': format_price(price_product_str),
            'desc': desc_product,
            'brand': brand,
            'size': list(sizes),
            'color': list(colors),
            'img': list(imgs)
        }

    def scrape_urls_products(self):
        # Creo instancia de browser debido a que al realizar por bs4 se obtiene una cantidad acotada de urls
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=self.options)

        driver.get(self.pathname)
        driver.implicitly_wait(10)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'lxml')
        driver.quit()

        unique_urls = set()
        for item in soup.find_all('script', type='application/ld+json'):
            json_data = json.loads(item.string)
            url_product = json_data.get('offers',{}).get('url')
            if url_product:
                unique_urls.add(url_product)

        return unique_urls
