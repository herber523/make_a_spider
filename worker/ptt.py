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

def last_page(board):
    res = requests.get(
            url= 'https://www.ptt.cc/bbs/' + board + '/index.html',
            cookies={'over18': '1'}
        ).text
    #last_page = res.split('上頁')[0].split('最舊')[1].split('/bbs/'+board+'/index')[1].split('.html')[0]
    page_num = re.findall(r'index(\w+).html', res)
    if not page_num:
        return 1
    last_page = int(page_num[1]) + 1
    return(last_page)

def page_parse(board,start,end):
    job = Job()
    for i in range(int(start),int(end)+1):
        job.add_job('ptt',data_parse,'https://www.ptt.cc/bbs/' + board + '/index%d.html' % i)

def data_parse(url):
    print(url)
    job = Job()
    page_data = []
    res = requests.get(
        url = url,
        cookies={ 'over18': '1'}
    ).text
    
    soup = BeautifulSoup(res,'lxml')
    row = soup.select('.r-ent')
    for r in row:
        url = r.select('a')[0]['href']
        job.add_job('ptt',body_parse,'https://www.ptt.cc'+url)


def body_parse(url):
    res = requests.get(
        url = url,
        cookies = {'over18': '1'}
        ).text
    soup = BeautifulSoup(res,'lxml')
    head_data = soup.select('.article-metaline')
    author = head_data[0].select('span')[1].text
    title = head_data[1].select('span')[1].text
    date = head_data[2].select('span')[1].text
    body = soup.text.split(date)[1].split('※ 發信站')[0]
    data = {
        'authou': author,
        'title': title,
        'date': date,
        'body': body
    }
    data = json.dumps(data)
    print(title)
    r.lpush('ptt',data)

def return_data():
    all_data = []

    while True:
        time.sleep(2)
        print('wait', r.get('waitjob'),'over', r.get('overjob'))
        if r.get('waitjob') == r.get('overjob'):
            break
        else:
            print('wait')

    data = r.lrange('ptt',0,-1)
    for d in data:
        all_data.append(json.loads(d.decode('utf-8')))
    r.delete('ptt')
    return json.dumps(all_data)

def run(board,start=0,end=-1):
    if end == -1:
        end = last_page(board)

    page_parse(board,start,end)
    return return_data()
