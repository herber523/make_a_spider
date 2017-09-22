import sys
import requests
from bs4 import BeautifulSoup
import json
from multiprocessing import Pool
import time
import re
sys.path.append('..')
from job.job import Job
import redis
r = redis.Redis()

def parse(start,end):
    job =Job()
    if end == -1:
        url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=1'
        res= requests.get(url,headers={'Host': 'rent.591.com.tw','User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'})
        d = json.loads(res.text)
        end = int(d['records'].replace(",", ""))
    for i in range(start,end,30):
        if i == 0:
            i = 1
        url = 'https://rent.591.com.tw/home/search/rsList?is_new_list=1&type=1&kind=0&searchtype=1&region=1&firstRow='+str(i)+'&totalRows='+str(end)
        job.add_job('s591',data_parse,url)

    


def data_parse(url):
    res= requests.get(url,headers={'Host': 'rent.591.com.tw','User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'})
    data = json.loads(res.text)
    data = data['data']['data']
    data = json.dumps(data)
    r.lpush('s591',data)


def return_data():
    all_data = []

    while True:
        time.sleep(2)
        wait = int(r.get('waitjob'))
        over = int(r.get('overjob'))
        print('wait',over,'/',wait)
        if r.get('waitjob') == r.get('overjob'):
            time.sleep(2)
            break

    data = r.lrange('s591',0,-1)
    for d in data:
        all_data.append(json.loads(d.decode('utf-8')))
    r.delete('s591')
    return json.dumps(all_data)

def run(start,end):
    parse(start,end)
    return return_data()
