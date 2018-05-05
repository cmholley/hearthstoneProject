#!/usr/bin/env python 
# based on  http://stackoverflow.com/questions/7052947/split-95mb-json-array-into-smaller-chunks
# usage: python json-split filename.json
# produces multiple filename_0.json of 1.49 MB size

import json
import sys
import os

filename, extension = os.path.splitext(sys.argv[1])
partitions = int(sys.argv[2])
with open(sys.argv[1],'r') as infile:
    o = json.load(infile)
    games = o["games"]
    chunkSize = len(games)/partitions
    for i in xrange(partitions-1):
        with open(filename+'_'+str(i+1)+extension, 'w') as outfile:
            data = games[i*chunkSize:(i+1)*chunkSize]
            json.dump(data, outfile)
    with open(filename + '_' + str(partitions) + extension, 'w') as outfile:
        data = games[(partitions-1) * chunkSize:]
        json.dump(data, outfile)
