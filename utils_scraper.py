def format_price(price):
    res = price.replace('$', '').replace('.', '').replace(',', '')
    return float(res)