import redis
class Boss():
    def __init__(self):
        self.r = redis.Redis(host='localhost',port=6379,db=0)
    def run(self,thread_num=4):
        r = self.r
        while True:
            job = r.blpop('job')
            jstr = job[1].decode('utf-8').split(';')
            j_func = jstr[0]
            j_arg = jstr[1]
            eval(j_func)(j_arg)
