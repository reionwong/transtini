import requests
from epc.server import EPCServer
from bs4 import BeautifulSoup

session = requests.Session()
server = EPCServer(('localhost', 0))

@server.register_function
def youdao_query(text):
    url = 'https://www.youdao.com/result'
    url_params = {"lang": "en", "word": text}
    r = session.get(url, params=url_params)
    raw_data = r.text
    bs = BeautifulSoup(raw_data, 'html.parser')
    result_data = text + '\n\n'

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

    return result_data

if __name__ == '__main__':
    server.print_port()
    server.serve_forever()
