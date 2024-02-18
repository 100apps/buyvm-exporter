import json
import re
from threading import Thread
import requests
from bs4 import BeautifulSoup


def request_buyvm(index, result):
    soup = BeautifulSoup(requests.get(f'https://my.frantech.ca/cart.php?gid={index}').text, 'html.parser')
    for div in soup.select('div.products .col-lg-4'):
        stock = 10000
        try:
            stock = int(re.findall(r"(\d*) Available", div.select_one('.package-qty').get_text())[0])
        except:
            pass
        info = {'zone': div.select_one('.package-name').get_text().split(" ")[0],
                'package_name': div.select_one('.package-name').get_text(),
                'price': float(re.findall(r"(\d+\.\d+) USD", div.select_one('.price').get_text())[0]),
                'stock': stock}
        result.append(info)


def get_results():
    result = []
    thread_array = []
    for i in [37, 38, 48, 39, 42, 49, 45, 46]:
        t = Thread(target=request_buyvm, args=(i, result,))
        thread_array.append(t)
        t.start()
    for t in thread_array:
        t.join()
    return result


if __name__ == '__main__':
    print(json.dumps(get_results(), indent=2))
