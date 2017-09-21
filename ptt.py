import argparse
import json
import worker.ptt as ptt
parser = argparse.ArgumentParser()
parser.add_argument('-o',help='filename')
parser.add_argument('-b',help='board')
parser.add_argument('-s',help='start page')
parser.add_argument('-e',help='end page')
args = parser.parse_args()
if not args.o:
    print('plase input output file name')
if not args.s:
    print('plase input start page')
if not args.e:
    print('plase input end page')
if not args.b:
    print('plase input board name')
board = args.b
start = int(args.s)
end = int(args.e)
filename = args.o
data = ptt.run(board,start,end)
data = json.loads(data)
with open(filename+'.json', 'w') as outfile:
    json.dump(data, outfile)
