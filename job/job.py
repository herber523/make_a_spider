import redis

class Job():
    def __init__(self):
        self.r = redis.Redis()        
    
    def add_job(self,f,function,arg):
        r = self.r
        f_name = function.__name__
        job_msg = f+'.'+f_name + ';' + arg
        r.incr('waitjob')
        r.lpush('job', job_msg)
