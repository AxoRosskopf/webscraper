from utils import generate_urls_from_product_page, generate_product_details, generate_csv_products


def main():
    urls= [
        {
            'brand': 'silenzio',
            'url':'https://silenzio.com.ar/productos?mpage=16'
        },
        {
            'brand': 'blancblanc',
            'url': 'https://www.blancblanc.com.ar/productos?mpage=7'
        },
        {
            'brand': 'codex',
            'url': 'https://www.codexstore.com.ar/productos/?mpage=5'
        },
        {
            'brand': 'altelierdelcroix',
            'url':'https://www.atelierdelcroix.com/productos?mpage=5'
        },
        {
            'brand': 'lalawhite',
            'url': "https://lalawhiteoficial.com/productos?mpage=3"
        },
        {
            'brand': 'real',
            'url': 'https://real-argentina.com.ar/productos/?mpage=4'
        },
        {
            'brand': 'cheijlab',
            'url': 'https://www.cheijlab.com/productos?mpage=3'
        },
        {
            'brand': 'reorient',
            'url': 'https://www.reorientba.com/productos?mpage=3'
        },
        {
            'brand': 'chaina',
            'url': 'https://www.chaina.com.ar/productos?mpage=3'
        },
        {
            'brand': 'bluming',
            'url': 'https://www.bluming.com.ar/productos/?sort_by=best-selling&mpage=11'
        },
        {
            "brand":"anima basics",
            "url":"https://www.animabasics.com/productos"
        },
        {
            "brand": "anima basics",
            "url":"https://www.animabasics.com/productos/page/2/"
        },
        {
            "brand": "anima basics",
            "url": "https://www.animabasics.com/productos/page/3/"
        },
        {
            "brand": "anima basics",
            "url": "https://www.animabasics.com/productos/page/3/"
        },
        {
            "brand": "anima basics",
            "url": "https://www.animabasics.com/productos/page/4/"
        },
        {
            "brand": "will ba",
            "url": "https://willba.mitiendanube.com/productos?mpage=33"
        },
        {
            "brand": "san martin",
            "url": "https://www.sanmartinargentina.com/productos?mpage=5"
        },
        {
            "brand":"gente di strada",
            "url": "https://gentedistrada.com.ar/productos"
        },
        {
            "brand": "aynie",
            "url": "https://ayniebsas.com.ar/categoria/carteras/"
        },
        {
            "brand": "aynie",
            "url": "https://ayniebsas.com.ar/categoria/accesorios/"
        },
        {
            "brand": "aynie",
            "url": "https://ayniebsas.com.ar/categoria/sombreros/"
        },
        {
            "brand": "aynie",
            "url": "https://ayniebsas.com.ar/categoria/noche/"
        },
        {
            "brand": "aynie",
            "url": "https://ayniebsas.com.ar/categoria/noche/"
        },
        {
            "brand": "elemental",
            "url": "https://elemental-ba.com/productos"
        },
        {
            "brand": "elemental",
            "url": "https://elemental-ba.com/productos/page/2/"
        },
        {
            "brand": "resistance",
            "url": "https://resistance4.mitiendanube.com/productos?mpage=5"
        }

    ]



    for i in urls:
        generate_urls_from_product_page(i.get('url'), i.get('brand'))

    for i in urls:
        generate_product_details(i.get('brand'))

    generate_csv_products(output_csv='./data/csv/products.csv', brand_csv='./data/csv/brands.csv')

if __name__ == '__main__':
    main()