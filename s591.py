import argparse
import json
import worker.s591 as s591
parser = argparse.ArgumentParser()
parser.add_argument('-o',help='filename')
parser.add_argument('-e',help='end page')
parser.add_argument('-s',help='start page')

args = parser.parse_args()
if not args.o:
    print('plase input output file name')
if not args.e:
    print('plase input end page')
if not args.s:
    print('plase input start page')



filename = args.o
end = int(args.e)
start = int(args.s)
data = s591.run(start,end)
data = json.loads(data)
with open(filename+'.json', 'w') as outfile:
    json.dump(data, outfile)
