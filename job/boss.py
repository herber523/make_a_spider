import sys
import redis
import time
from multiprocessing import Pool
sys.path.append('..')
import worker.ptt as ptt
r = redis.Redis()


class Boss():
    def __init__(self,process=4):
        self.r = redis.Redis(host='localhost',port=6379,db=0)
        self.pool = Pool(processes=process)
        self.r.delete('job')
        self.r.delete('waitjob')
        self.r.delete('overjob')
        print('init')
    def run(self):
        r = self.r
        while True:
            job = r.brpop('job')
            jstr = job[1].decode('utf-8').split(';')
            j_func = jstr[0]
            j_arg = jstr[1]
            print(j_arg)
            self.pool.apply_async(run_func,args=(j_func,j_arg,))



def run_func(func_name,func_arg):
    r.incr('overjob')
    eval(func_name)(func_arg)
