import requests
import requests_cache
from epc.server import EPCServer
from bs4 import BeautifulSoup

# session = requests.Session()
session = requests_cache.CachedSession(
    'transtini_cache',
    use_cache_dir=True,
    cache_control=True,
    expire_after=timedelta(days=30)
)
server = EPCServer(('localhost', 0))

@server.register_function
def youdao_query(text):
    url = 'https://www.youdao.com/result'
    url_params = {"lang": "en", "word": text}
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}

    r = session.get(url, params=url_params, headers=headers)
    raw_data = r.text
    bs = BeautifulSoup(raw_data, 'html.parser')
    result_data = ''

    tag_phonetic = bs.select_one('.phone_con')
    if tag_phonetic != None:
        for i in tag_phonetic.select('.per-phone'):
            result_data += (i.text + '\n')
        result_data += '\n'

    tag_explains = bs.select_one('.trans-container>ul')
    if tag_explains != None:
        for i in tag_explains.select('.word-exp'):
            result_data += (i.text + '\n')
        result_data += '\n'

    tag_trans_content = bs.select_one('.trans-container>p')
    if tag_trans_content != None:
        for i in tag_trans_content:
            result_data += (i.text + '\n')

    if result_data == '':
        result_data = '抱歉，没有找到相关的内容'

    return text + "\n\n" + result_data

if __name__ == '__main__':
    server.print_port()
    server.serve_forever()
