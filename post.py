import os
import time

import requests

import jikipedia
from rich.console import Console
from rich.table import Table
console = Console()

phone = input("你的手机号：")
pwd = input("你的密码：")
jiki = jikipedia.Jikipedia(phone, pwd)
page = 1
old_d = {}
try:
    os.makedirs('./jikipedia_backup_post/')
except FileExistsError:
    pass
while True:
    data = jiki.request_created_definition(page=page, category="post")
    if old_d == data:
        break
    else:
        try:
            if data['category'] != 'ban_enabled':
                old_d = data.copy()
        except KeyError:
            old_d = data.copy()
    console.rule(f'正在获取第 {page} 页数据')
    console.print(data)
    try:
        for d in data['data']:
            work_pwd = f'./jikipedia_backup_post/{d["id"]}-{d["term"]["title"]}'
            try:
                os.makedirs(work_pwd)
            except FileExistsError:
                continue
            except OSError:
                work_pwd = f'./jikipedia_backup_post/{d["id"]}'
                try:
                    os.makedirs(work_pwd)
                except FileExistsError:
                    continue
            with open(f'{work_pwd}/plaintext.txt', 'w', encoding='UTF-8') as f:
                f.write(d['plaintext'])
            with open(f'{work_pwd}/content.txt', 'w', encoding='UTF-8') as f:
                f.write(d['content'])
            with open(f'{work_pwd}/url.txt', 'w', encoding='UTF-8') as f:
                ref_uri = []
                for ref in d['references']:
                    ref_uri.append(f"{ref['title']} - {ref['path']}")
                f.write('\n'.join(ref_uri))
            for img in d['images']:
                with open(f'{work_pwd}/{img["full"]["path"].split("/")[-1]}', 'wb') as f:
                    f.write(requests.get(img['full']['path']).content)
            table = Table()
            console.print(d)
    except KeyError:
        console.rule('Error: 请求过多')
        time.sleep(60)
    time.sleep(1)
    page += 1
