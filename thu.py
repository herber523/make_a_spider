import argparse
import json
import worker.thu as thu
parser = argparse.ArgumentParser()
parser.add_argument('-o',help='filename')
parser.add_argument('-y',help='year')
parser.add_argument('-s',help='semester')

args = parser.parse_args()
if not args.o:
    print('plase input output file name')
if not args.y:
    print('plase input year')
if not args.s:
    print('plase input semester')



filename = args.o
year = args.y
semester = args.s
data = thu.run(year,semester)
data = json.loads(data)
with open(filename+'.json', 'w') as outfile:
    json.dump(data, outfile)
