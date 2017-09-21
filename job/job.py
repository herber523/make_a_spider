import redis

class Job():
    def __init__(self):
        self.r = redis.Redis(host='localhost',port=6379,db=0)        
    
    def proc_async(self,function,arg):
        r = self.r
        f_name = function.__name__
        job_msg = f_name + ';' + arg
        r.lpush('job', job_msg)
