from job.boss import Boss
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-c')
args = parser.parse_args()
if not args.c:
    print('plase input process num')

Boss(int(args.c)).run()
