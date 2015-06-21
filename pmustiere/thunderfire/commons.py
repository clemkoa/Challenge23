#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import matplotlib.pyplot as plt
from math import log, pow, exp, sqrt, pi

numCat = 15
catsToIDs = {1: 0, 2: 1, 10: 2, 15: 3, 17: 4, 19: 5, 20: 6, 22: 7, 23: 8, 24: 9, 25: 10, 26: 11, 27: 12, 28: 13, 29: 14}
IDsToCats = {0: 1, 1: 2, 2: 10, 3: 15, 4: 17, 5: 19, 6: 20, 7: 22, 8: 23, 9: 24, 10: 25, 11: 26, 12: 27, 13: 28, 14: 29}

accuracyTopics = 66.35399162298413
accuracyWords = 66.31637029419879
accuracyWordLinks = 84.08048601943327

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

def readRow(row, a):
        if a >= 4 and a <= 8:
            return int(row[a])
        elif a == 9:
            return readDuration(row[9])
        elif a == 10:
            if row[10] == '3d':
                return 1.0
            elif row[10] == '2d':
                return 0.0
            else:
                print('ERROR in dimension : Unexpected value {}'.format(row[10]))
                return -1.0
        elif a == 11:
            if row[11] == 'hd':
                return 1.0
            elif row[11] == 'sd':
                return 0.0
            else:
                print('ERROR in definition : Unexpected value {}'.format(row[11]))
                return -1.0
        elif a == 12:
            if row[12] == 'true':
                return 1.0
            elif row[12] == 'false':
                return 0.0
            else:
                print('ERROR in caption : Unexpected value {}'.format(row[12]))
                return -1.0
        elif a == 13:
            if row[13] == 'True':
                return 1.0
            elif row[13] == 'False':
                return 0.0
            else:
                print('ERROR in definition : Unexpected value {}'.format(row[13]))
                return -1.0

def parseTopicIDS(topicIDS):
    m = topicIDS.split(';')
    if m:
        return m
    else:
        if topicIDS == "":
            return []
        else:
            return [].append(topicIDS)

def getWordsFromSentence(sentence):
    s = ''
    addedSpace = True
    for l in sentence.lower():
        if l.isalnum():
            s += l
            addedSpace = False
        elif not addedSpace:
            s += ' '
            addedSpace = True

    if addedSpace and s != '':
        s = s[:-1]

    return s.split(' ')

