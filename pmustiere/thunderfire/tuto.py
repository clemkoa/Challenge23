from commons import *
from read import *
from use import *

tfTopics, idfTopics, tfWords, idfWords, tfWordLinks, idfWordLinks, valueMeans, valueEcarts = calcTFIDF(sampling=True)

resultTopics, decisionTopics, a = useTFIDF(0, tfTopics, idfTopics, sampling=True)
resultWords, decisionWords, a = useTFIDF(1, tfWords, idfWords, sampling=True)
resultWordLinks, decisionWordLinks, a = useTFIDF(2, tfWordLinks, idfWordLinks, sampling=True)

aggregatedDecisions = computeAggregated(decisionTopics, accuracyTopics, decisionWords, accuracyWords, decisionWordLinks, accuracyWordLinks)
realDecisions = convertAggregatedDecisions(aggregatedDecisions)

for d in realDecisions:
    print(d)
