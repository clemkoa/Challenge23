#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from math import log, pow, exp

def parseLine(line):
    if line[0] == ',':
        line = line[1:]

    l = []
    start = 0
    inQuotes = False
    hasQuotes = False
    for i in range(len(line)):
        if line[i] == '"':
            inQuotes = not inQuotes
            hasQuotes = True
        elif line[i] == ',' and not inQuotes:
            if hasQuotes:
                v = line[start+1:i-1]
                l.append(v.replace('""', '"'))
            else:
                l.append(line[start:i])
            start = i+1
            hasQuotes = False
            inQuotes = False

    if hasQuotes:
        v = line[start+1:-2] # Because of \n
        l.append(v.replace('""', '"'))
    else:
        l.append(line[start:-1]) # Because of \n

    return l

def readDuration(s):
    duration = 0

    if s == 'NA' or s == '':
        return 0

    #print(s)
    s = s[1:] # Remove the 'P'

    if s[0] != 'T':
        i = 0
        while s[i] != 'D':
            i += 1

        val = s[0:i]
        
        #print('Days : {}'.format(val))
        duration += val*24*3600

        s = s[i+1:]
    
    s = s[1:] # Remove the 'T'
    #print(s)

    while s != '':
        i = 0
        while s[i] != 'H' and s[i] != 'M' and s[i] != 'S':
            i += 1
        
        val = int(s[0:i])
        
        if s[i] == 'H':
            #print('Hours : {}'.format(val))
            duration += val*3600
        elif s[i] == 'M':
            #print('Minutes : {}'.format(val))
            duration += val*60
        elif s[i] == 'S':
            #print('Seconds : {}'.format(val))
            duration += val

        s = s[i+1:]

    #print('Duration : {}'.format(duration))
    return duration

def parseTopicIDS(topicIDS):
    m = topicIDS.split(';')
    if m:
        return m
    else:
        if topicIDS == "":
            return []
        else:
            return [].append(topicIDS)

r = open('data/train_sample.csv', 'r', newline='', encoding='utf-8')

numCat = 15
catsToIDs = {1: 0, 2: 1, 10: 2, 15: 3, 17: 4, 19: 5, 20: 6, 22: 7, 23: 8, 24: 9, 25: 10, 26: 11, 27: 12, 28: 13, 29: 14}
IDsToCats = {0: 1, 1: 2, 2: 10, 3: 15, 4: 17, 5: 19, 6: 20, 7: 22, 8: 23, 9: 24, 10: 25, 11: 26, 12: 27, 13: 28, 14: 29}

catRows = [[] for i in range(numCat)]
catTopics = [{} for i in range(numCat)]
catCounts = [0 for i in range(numCat)]

i = 0
start = time.clock()
for line in r.readlines():
    if i == 0:
        i += 1
        continue

    #print(i)
    row = parseLine(line)
    row[0] = int(row[0])
    row[9] = readDuration(row[9])
    
    row[14] = parseTopicIDS(row[14])
    row[15] = parseTopicIDS(row[15])

    catID = catsToIDs[row[0]]
    catRows[catID].append(row)

    for topic in row[14]+row[15]:
        if topic not in catTopics[catID]:
            catTopics[catID][topic] = 1
        else:
            catTopics[catID][topic] += 1
        catCounts[catID] += 1
    
    i += 1
r.close()

print('Took {}s'.format(time.clock()-start))

differentTopics = {}
for i in range(len(catRows)):
    for t in catTopics[i]:
        differentTopics[t] = 0

sumRows = 0
for i in range(len(catRows)):
    sumRows += len(catRows[i])
    for t in catTopics[i]:
        differentTopics[t] += 1

    print('Cat {} has {} elements'.format(IDsToCats[i], len(catRows[i])))
    print('has {} different topics'.format(len(catTopics[i])))
print()
print('Total elements : {}'.format(sumRows))
print('Total different topics : {}'.format(len(differentTopics)))
print()
print()

for k in differentTopics.keys():
    differentTopics[k] = log(numCat/differentTopics[k])


r = open('data/test_sample.csv', 'r', newline='', encoding='utf-8')
w = open('results.csv', 'w')

i = 0
start = time.clock()
w.write('id;video_category_id\n')
nothingCount = 0
newTopics = {}
for line in r.readlines():
    if i == 0:
        i += 1
        continue

    #print(i)
    line = line.replace('\\"', '""')
    row = parseLine(line)

    testID = int(row[0])
    row[9] = readDuration(row[9])
    
    row[14] = parseTopicIDS(row[14])
    row[15] = parseTopicIDS(row[15])

    topics = row[14] + row[15]

    scores = [0 for k in range(numCat)]

    for t in topics:
        for k in range(numCat):
            if t in catTopics[k]:
                scores[k] += catTopics[k][t]/catCounts[k] * differentTopics[t]
            elif t not in newTopics:
                newTopics[t] = 1


    nothing = True
    for i in range(numCat):
        if scores[i] != 0:
            nothing = False

    if nothing:
        nothingCount += 1

    maxScore = scores[0]
    maxID = 0
    for k in range(1, numCat):
        if scores[k] > maxScore:
            maxScore = scores[k]
            maxID = k

    w.write('{};{}\n'.format(testID, IDsToCats[maxID]))

    i += 1
r.close()
w.close()

print('Unsortable test elements : {}'.format(nothingCount))
print('New different topics : {}'.format(len(newTopics)))
