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

def parse(year,semester):
    job =Job()
    url = 'http://course.thu.edu.tw/view-dept/'+str(year)+'/'+str(semester) +'/everything'
    res = requests.get(url)
    domain = 'http://course.thu.edu.tw'
    res = BeautifulSoup(res.text,'lxml')
    for dp in res.select('tr a'):
        dp_url = domain + dp['href']
        job.add_job('thu', dp_parse, dp_url)



def dp_parse(url):
    res = requests.get(url)
    res = BeautifulSoup(res.text,'lxml')
    courses = res.select('.aqua_table tbody tr')
    for c in courses:
        item = {}
        item['id'] = c.select('td')[0].text.strip()
        item['name'] = c.select('td')[1].text.strip()
        item['credit'] = c.select('td')[2].text.strip()
        item['time'] = c.select('td')[3].text.strip()
        item['teacher'] = c.select('td')[4].text.strip()
        item['num'] = c.select('td')[5].text.strip()
        item['department'] = c.select('td')[6].select('a')[0].text.strip()
        item['note'] = c.select('td')[6].text.strip()
        data = json.dumps(item)
        print(item['name'])
        r.lpush('thu',data)


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

    data = r.lrange('thu',0,-1)
    for d in data:
        all_data.append(json.loads(d.decode('utf-8')))
    r.delete('thu')
    return json.dumps(all_data)

def run(year,semester):
    parse(year,semester)
    return return_data()
