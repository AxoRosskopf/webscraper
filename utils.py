import threading
import os
import csv
import json
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
import scraper
import sys
import time

def loading_spinner(stop_event):
    earth = ['🌍', '🌎', '🌏']
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\rLoading {earth[idx % len(earth)]}")
        sys.stdout.flush()
        time.sleep(0.2)
        idx += 1
    sys.stdout.write('\n')

def generate_urls_from_product_page(url, brand):
    print(f"Scraping urls from : {brand}")
    bob_scraper = scraper.ProductScraper(pathname=url)
    json_file_path =  f'./url_precomputed/{brand}_urls.json'
    if os.path.exists(json_file_path):
        print(f"URLs already scraped : {brand}")
    else:
        unique_urls = set()
        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=loading_spinner, args=(stop_event, ))
        spinner_thread.start()
        try:
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = {executor.submit(bob_scraper.scrape_urls_products): _ for _ in range(5)}

                for future in as_completed(futures):
                    try:
                        result = future.result()
                        unique_urls.update(result)
                    except Exception as e:
                        print(f"ERROR: {e}")
        finally:
            stop_event.set()
            spinner_thread.join()
            print(f"Finished scraping urls from {brand}")

        export_json(list(unique_urls), f'./url_precomputed/{brand}_urls.json')


def generate_csv_products(output_csv, brand_csv):
    json_files = [f for f in os.listdir('./data/json') if f.endswith('.json')]

    with open(brand_csv, mode='w', newline='', encoding='utf-8') as f:
        fieldnames = ['id', 'brand', 'products']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for json_file in json_files:
            brand_name = json_file.split('_')[0]
            with open(os.path.join('./data/json', json_file), 'r', encoding='utf-8') as json_f:
                data = json.load(json_f)
                product_ids = [str(product['id']) for product in data]
                writer.writerow({
                    'id': str(uuid.uuid4()),
                    'brand': brand_name,
                    'products': ', '.join(product_ids)
                })

    all_products = []

    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'name', 'price', 'description','brand', 'size', 'color', 'img']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for json_file in json_files:
            with open(os.path.join('./data/json', json_file), 'r', encoding='utf-8') as json_f:
                data = json.load(json_f)
                all_products.extend(data)

        for product in all_products:
            writer.writerow({
                'id': product.get('id'),
                'name': product.get('name'),
                'price': str(product.get('price')),
                'description': product.get('desc'),
                'brand': product.get('brand'),
                'size': product.get('size'),
                'color': product.get('color'),
                'img': product.get('img')
            })


def export_json(data, filename):
    with open(filename, mode='w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

def scrape_chunk_of_products(chunk, brand):
    results = []
    for url in chunk:
        bob_scraper = scraper.ProductScraper(pathname=url)
        try:
            product_detail = bob_scraper.scrape_product_detaiil(brand)
            results.append(product_detail)
        except Exception as e:
            print(f"Error scraping {url}: {e}")
    return results

def generate_product_details(brand):
    json_file_path = f'./url_precomputed/{brand}_urls.json'
    json_file_dst = f'./data/json/{brand}_products.json'

    if os.path.exists(json_file_path):
        print(f"URLs already scraped : {brand}")
    else:
        raise FileNotFoundError(f"The file {json_file_path} does not exist.")

    with open(json_file_path, 'r', encoding='utf-8') as f:
        urls_list = json.load(f)

    num_threads = 5
    chunk_size = max(1, len(urls_list) // num_threads)  # Ensure chunk_size is never zero

    result_products = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(scrape_chunk_of_products, urls_list[i:i + chunk_size], brand)
            for i in range(0, len(urls_list), chunk_size)
        ]
        for future in as_completed(futures):
            result_products.extend(future.result())

    export_json(result_products, json_file_dst)




