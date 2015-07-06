#!/usr/bin/env python
# -*- coding: utf-8 -*-

from commons import *

def calcTFIDF(sampling=False, numSampling=2, testSample=0):
    r = open('../../challenge_23_data/train_sample.csv', 'r', newline='', encoding='utf-8')

    catTopics = [{} for i in range(numCat)]
    catTopicCounts = [0 for i in range(numCat)]

    catWords = [{} for i in range(numCat)]
    catWordCounts = [0 for i in range(numCat)]

    numVal = 10
    values = [[[] for j in range(numCat)] for i in range(numVal)]
    valueCounts = [[0 for j in range(numCat)] for i in range(numVal)]
    valueSum = [[0.0 for j in range(numCat)] for i in range(numVal)]
    valueSumSq = [[0.0 for j in range(numCat)] for i in range(numVal)]

    i = -1
    for line in r.readlines():
        if i == -1:
            i += 1
            continue

        """if i > 15:
            break"""

        if sampling and (i%numSampling == testSample):
            i += 1
            continue

        row = parseLine(line)
        catID = catsToIDs[int(row[0])]
        topics = parseTopicIDS(row[14]) + parseTopicIDS(row[15])
        words = getWordsFromSentence(row[1]) + getWordsFromSentence(row[2])

        for a in range(4, 14):
            if row[a] != 'NA' and row[a] != '':
                v = readRow(row, a)
                values[a-4][catID].append(v)

                valueCounts[a-4][catID] += 1
                valueSum[a-4][catID] += float(v)
                valueSumSq[a-4][catID] += pow(float(v), 2.0)

        for topic in topics:
            if topic not in catTopics[catID]:
                catTopics[catID][topic] = 1
            else:
                catTopics[catID][topic] += 1
            catTopicCounts[catID] += 1

        for k in range(len(words)):
            w = words[k]
            nextW = ''
            if k+1 != len(words):
                nextW = words[k+1]
            prevW = ''
            if k-1 != -1:
                prevW = words[k-1]

            if w != '':
                catWordCounts[catID] += 1

                if w not in catWords[catID].keys():
                    catWords[catID][w] = [1, {nextW:1}, {prevW:1}]
                else:
                    catWords[catID][w][0] += 1
                    if nextW not in catWords[catID][w][1].keys():
                        catWords[catID][w][1][nextW] = 1
                    else:
                        catWords[catID][w][1][nextW] += 1
                    if prevW not in catWords[catID][w][2].keys():
                        catWords[catID][w][2][prevW] = 1
                    else:
                        catWords[catID][w][2][prevW] += 1
        
        i += 1
    r.close()

    tfTopics = [{topic: float(catTopics[catID][topic])/float(catTopicCounts[catID]) for topic in catTopics[catID].keys()} for catID in range(numCat)]

    idfTopics = {}
    for i in range(numCat):
        for t in catTopics[i]:
            idfTopics[t] = 0

    for i in range(numCat):
        for t in catTopics[i]:
            idfTopics[t] += 1

    for k in idfTopics.keys():
        idfTopics[k] = log(float(numCat)/float(idfTopics[k]))

    tfWords = [{word: float(catWords[catID][word][0])/float(catWordCounts[catID]) for word in catWords[catID].keys()} for catID in range(numCat)]

    idfWords = {}
    for i in range(numCat):
        for w in catWords[i]:
            idfWords[w] = 0

    for i in range(numCat):
        for w in catWords[i]:
            idfWords[w] += 1

    for k in idfWords.keys():
        idfWords[k] = log(float(numCat)/float(idfWords[k]))

    valueMeans = [[float(valueSum[a][i])/float(valueCounts[a][i]) for i in range(numCat)] for a in range(numVal)]
    valueEcarts = [[sqrt(float(valueSumSq[a][i])/float(valueCounts[a][i]) - pow(valueMeans[a][i], 2.0)) for i in range(numCat)] for a in range(numVal)]

    tfWordLinks = [{word: {word2: float(catWords[catID][word][1][word2])/float(catWords[catID][word][0]) for word2 in catWords[catID][word][1].keys()} for word in catWords[catID].keys()} for catID in range(numCat)]

    idfWordLinks = {}
    for i in range(numCat):
        for w in catWords[i].keys():
            if w not in idfWordLinks:
                idfWordLinks[w] = {}
            for w2 in catWords[i][w][1].keys():
                idfWordLinks[w][w2] = 0

    for i in range(numCat):
        for w in catWords[i].keys():
            for w2 in catWords[i][w][1].keys():
                idfWordLinks[w][w2] += 1

    for w in idfWordLinks:
        for k in idfWordLinks[w].keys():
            idfWordLinks[w][k] = log(float(numCat)/float(idfWordLinks[w][k]))

    toPlot = []#range(numVal)
    for a in toPlot:
        plt.title('Row : {}'.format(a+4))
        for i in range(numCat):
            plt.plot([valueMeans[a][i]-valueEcarts[a][i], valueMeans[a][i]+valueEcarts[a][i]], [i, i])
            plt.plot(values[a][i], [i+0.1 for j in range(len(values[a][i]))], 'o')
            print('{} +- {}'.format(valueMeans[a][i], valueEcarts[a][i]))
        plt.show()

    return tfTopics, idfTopics, tfWords, idfWords, tfWordLinks, idfWordLinks, valueMeans, valueEcarts