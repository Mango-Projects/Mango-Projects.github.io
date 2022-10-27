import tomllib
import os
import re

with open('./data.toml', 'rb') as file:
    data = tomllib.load(file)

url_base = lambda url: data['url_base'].format(url=url)
table_base = lambda domain, namespace, raw_url, transfer_url: \
    data['table_base'].format(domain=domain, namespace=namespace, raw_url=raw_url, transfer_url=transfer_url)
transfer_url_base = lambda url: data['transfer_url_base'].format(url=url)

with open('./index.md', 'w', encoding='utf8') as index_file:
    index_file.write(data['markdown_base'])

for d_k, d_v in data.items():
    if 'base' in d_k:
        continue
    if not os.path.isdir(f'./{d_k}'):
        os.mkdir(f'./{d_k}')
    for v_k, v_v in d_v.items():
        filename = re.match(r'(?:www)?\.(.+)\.', v_k).group(1)
        url = f'https://{v_k}{v_v}'
        with open(f'./{d_k}/{filename}.html', 'w', encoding='utf8') as file:
            file.write(url_base(url))
        with open('./index.md', 'a', encoding='utf8') as file:
            file.write(table_base(d_k, v_k+v_v, url, transfer_url_base(v_k+v_v)))
        