#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt
from math import log, pow, exp

numCat = 15
catsToIDs = {1: 0, 2: 1, 10: 2, 15: 3, 17: 4, 19: 5, 20: 6, 22: 7, 23: 8, 24: 9, 25: 10, 26: 11, 27: 12, 28: 13, 29: 14}
IDsToCats = {0: 1, 1: 2, 2: 10, 3: 15, 4: 17, 5: 19, 6: 20, 7: 22, 8: 23, 9: 24, 10: 25, 11: 26, 12: 27, 13: 28, 14: 29}

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

def calcTFIDF(sampling=False, numSampling=2, testSample=0):
    r = open('data/train_sample.csv', 'r', newline='', encoding='utf-8')

    catTopics = [{} for i in range(numCat)]
    catCounts = [0 for i in range(numCat)]

    i = -1
    for line in r.readlines():
        if i == -1:
            i += 1
            continue

        if sampling and (i%numSampling == testSample):
            i += 1
            continue

        row = parseLine(line)
        catID = catsToIDs[int(row[0])]
        topics = parseTopicIDS(row[14]) + parseTopicIDS(row[15])

        for topic in topics:
            if topic not in catTopics[catID]:
                catTopics[catID][topic] = 1
            else:
                catTopics[catID][topic] += 1
            catCounts[catID] += 1
        
        i += 1
    r.close()

    tfTopics = [{topic: float(catTopics[catID][topic])/float(catCounts[catID]) for topic in catTopics[catID].keys()} for catID in range(numCat)]

    idfTopics = {}
    for i in range(len(catTopics)):
        for t in catTopics[i]:
            idfTopics[t] = 0

    for i in range(len(catTopics)):
        for t in catTopics[i]:
            idfTopics[t] += 1

    for k in idfTopics.keys():
        idfTopics[k] = log(float(numCat)/float(idfTopics[k]))

    return tfTopics, idfTopics

def useTFIDF(tfTopics, idfTopics, sampling=False, numSampling=2, testSample=0):
    if sampling:
        r = open('data/train_sample.csv', 'r', newline='', encoding='utf-8')

        ok = 0
        notOk = 0
        confusionMatrix = [[0 for j in range(numCat)] for i in range(numCat)]

        xs1 = []
        xs2 = []
        ys1 = []
        ys2 = []
    else:
        r = open('data/test_sample.csv', 'r', newline='', encoding='utf-8')
        w = open('results.csv', 'w')
        w.write('id;video_category_id\n')

    i = -1     
    for line in r.readlines():
        if i == -1:
            i += 1
            continue

        if sampling and (i%numSampling != testSample):
            i += 1
            continue

        if not sampling:
            line = line.replace('\\"', '""')
            row = parseLine(line)
            testID = int(row[0])
        else:
            row = parseLine(line)
            catID = catsToIDs[int(row[0])]
        topics = parseTopicIDS(row[14]) + parseTopicIDS(row[15])

        scores = [0 for k in range(numCat)]

        for t in topics:
            for k in range(numCat):
                if t in tfTopics[k]:
                    scores[k] += tfTopics[k][t] * idfTopics[t]

        maxScore = scores[0]
        maxID = 0
        for k in range(1, numCat):
            if scores[k] > maxScore:
                maxScore = scores[k]
                maxID = k

        if sampling:
            confusionMatrix[catID][maxID] += 1

            if maxID == catID:
                ok += 1
            else:
                notOk += 1
        else:
            w.write('{};{}\n'.format(testID, IDsToCats[maxID]))

        i += 1
    r.close()
    
    if sampling:
        accuracy = 100.0 * float(ok) / float(ok+notOk)
        print('Accuracy : {}'.format(accuracy))
        print('Confusion matrix :')
        i = 0
        for v in confusionMatrix:
            s = 0
            for a in v:
                s += a

            for a in v:
                print('{}\t'.format(a), end="")
            print('Recall : {}'.format(100.0*float(confusionMatrix[i][i])/float(s)))
            print()
            i += 1
    else:
        w.close()


start = time.clock()
print('Computing TF-IDF...')
tfTopics, idfTopics = calcTFIDF(sampling=True)
print('Done in {}s'.format(time.clock()-start))

start = time.clock()
print('Using TF-IDF...')
useTFIDF(tfTopics, idfTopics, sampling=True)
print('Done in {}s'.format(time.clock()-start))
