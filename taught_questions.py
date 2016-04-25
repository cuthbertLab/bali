# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

import copy

#from pprint import pprint as print
import bali
fp = bali.FileParser()
'''
Try to prove hypothesis that Lanang strokes are on the beat and Wadon strokes
are off the beat

Starting with hypothesis that only high strokes (e and o) are being analyzed
'''

'''
What percentage of Lanang and Wadon is on and off the beat? 
'''



def percentOnBeatTaughtList(listOfPatterns, typeOfStroke='e'):
    '''
    Returns percent on beat for a certain type of stroke for every pattern in
    a list of patterns. Organized as a dictionary with pattern as key and 
    percent on beat as value
    
    >>> import bali, taught_questions
    >>> fp = bali.FileParser()
    >>> lanangPatterns = fp.separatePatternsByDrum()[0]
    >>> percentlist = taught_questions.percentOnBeatTaughtList(lanangPatterns, 'e')
    >>> len(lanangPatterns)
    41
    >>> len(percentlist)
    41
    >>> percentlist[1]
    85.7...
    '''
    percents = []
    for i in range(len(listOfPatterns)):
        percents.append(listOfPatterns[i].percentOnBeatTaught(typeOfStroke))
    return percents

'''
Figure out if this "Lanang on beat, Wadon off beat" hypothesis doesn't hold with double strokes
'''

def singleStrokes(listOfPatterns, typeOfStroke='e'):
    '''
    Finds patterns that only have single strokes for the type of stroke and returns them in a list
    This method is obsolete
    
    >>> import bali, taught_questions
    >>> fp = bali.FileParser()
    >>> lanangPatterns = fp.separatePatternsByDrum()[0]
    >>> len(taught_questions.singleStrokes(lanangPatterns, 'e'))
    5
    '''
    singleStrokePatterns = []
    for pattern in listOfPatterns:
        doubleStrokes = 0
        strokes = list(pattern.drumPattern.replace(' ', ''))
        for i in range(len(strokes) - 1):
            if strokes[i] == strokes[i + 1] and strokes[i] != '_':
                doubleStrokes += 1
        if doubleStrokes == 0:
            singleStrokePatterns.append(pattern)
    return singleStrokePatterns

def consecutiveStrokes(listOfPatterns, typeOfStroke='eo'):
    '''
    Finds patterns that only have single strokes for the type of stroke and returns them in a list
    This method is obsolete
    
    >>> import bali, taught_questions
    >>> fp = bali.FileParser()
    >>> lanangPatterns, wadonPatterns = fp.separatePatternsByDrum()
    >>> len(taught_questions.consecutiveStrokes(lanangPatterns, 'e'))
    36
    >>> len(taught_questions.consecutiveStrokes(lanangPatterns, 'Tl'))
    2
    >>> len(taught_questions.consecutiveStrokes(wadonPatterns, 'o'))
    15
    
    Default is to check for either e or o
    
    >>> len(taught_questions.consecutiveStrokes(wadonPatterns, 'eo'))
    15
    >>> len(taught_questions.consecutiveStrokes(wadonPatterns))
    15
    '''
    doubleStrokePatterns = []
    for pattern in listOfPatterns:
        doubleStrokes = 0
        strokes = list(pattern.drumPattern.replace(' ', ''))
        for i in range(len(strokes) - 1):
            if strokes[i] not in typeOfStroke:
                continue
            if strokes[i] == strokes[i + 1] and strokes[i] != '_':
                doubleStrokes += 1
        if doubleStrokes > 0:
            doubleStrokePatterns.append(pattern)
    return doubleStrokePatterns

def removeSingleStrokes(pattern, typeOfStroke='e'):
    '''
    Returns drum pattern with all single strokes of a given type removed
    The single strokes are replaced with ','

    >>> import bali, taught_questions
    >>> fp = bali.FileParser()
    >>> pattern = fp.taught[4]
    >>> pattern
    <bali.Taught Pak Dewa Lanang 10:(_)e e T e _ _ _ _ e e _ e _ e _ _>
    
    >>> removed = taught_questions.removeSingleStrokes(pattern, 'e')
    >>> removed
    <bali.Taught Pak Dewa Lanang 10:(_)e e T , _ _ _ _ e e _ , _ , _ _>
    >>> removed.percentOnBeatTaught('e')
    50.0
    '''
    newDrumPatternList = copy.deepcopy(pattern.strokes)
    for i in range(1, len(pattern.strokes) - 1):
        if pattern.strokes[i] != pattern.strokes[i + 1] and pattern.strokes[i] == typeOfStroke:
            if pattern.strokes[i - 1] != typeOfStroke:
                newDrumPatternList[i] = ','
                
    newDrumPattern = copy.deepcopy(pattern)
    newDrumPattern.strokes = newDrumPatternList
    
    return newDrumPattern
    
def removeConsecutiveStrokes(pattern, typeOfStroke='e', removeFirst=True, removeSecond=False):
    '''
    Returns drum pattern with first stroke of a double stroke of a given type removed.
    
    The first stroke of a double stroke is replaced with '.'
    
    >>> import bali, taught_questions
    >>> fp = bali.FileParser()
    >>> pattern = fp.taught[4]
    >>> pattern
    <bali.Taught Pak Dewa Lanang 10:(_)e e T e _ _ _ _ e e _ e _ e _ _>
    
    >>> removed = taught_questions.removeConsecutiveStrokes(pattern, 'e')
    >>> removed
    <bali.Taught Pak Dewa Lanang 10:(_). e T e _ _ _ _ . e _ e _ e _ _>
    >>> removed.percentOnBeatTaught('e')
    100.0

    >>> removed2 = taught_questions.removeConsecutiveStrokes(pattern, 'e', removeSecond=True)
    >>> removed2
    <bali.Taught Pak Dewa Lanang 10:(_). . T e _ _ _ _ . . _ e _ e _ _>


    Not appearing in the repertoire except by mistake, but for completeness sake
    the name of this method is correct.  It removes all but the last even
    in cases where there are three or more in a row, unless removeSecond is True

    >>> pattern = fp.taught[4]
    >>> pattern.drumPattern = '(_)e e T e _ _ _ _ e e e _ _ e _ _'
    >>> removed = taught_questions.removeConsecutiveStrokes(pattern, 'e')
    >>> removed
    <bali.Taught Pak Dewa Lanang 10:(_). e T e _ _ _ _ . . e _ _ e _ _>
    
    
    Testing removing single strokes first, then removing first double strokes
    
    >>> pattern2 = fp.taught[7]
    >>> pattern2
    <bali.Taught Pak Tut Lanang Dasar 2:(_)e e _ _ e e _ e _ _ e e T _ T _>
    
    >>> removedSingle = taught_questions.removeSingleStrokes(pattern2, 'e')
    >>> removedSingle
    <bali.Taught Pak Tut Lanang Dasar 2:(_)e e _ _ e e _ , _ _ e e T _ T _>
    
    >>> removedSingle.percentOnBeatTaught('e')
    50.0
    
    >>> removedFirstDouble = taught_questions.removeConsecutiveStrokes(removedSingle, 'e')
    >>> removedFirstDouble
    <bali.Taught Pak Tut Lanang Dasar 2:(_). e _ _ . e _ , _ _ . e T _ T _>
    >>> removedFirstDouble.percentOnBeatTaught('e')
    100.0
    
    Testing removing both double strokes 
    
    >>> removedBothDoubles = taught_questions.removeConsecutiveStrokes(removedSingle, 'e', removeSecond=True)
    >>> removedBothDoubles
    <bali.Taught Pak Tut Lanang Dasar 2:(_). . _ _ . . _ , _ _ . . T _ T _>
    
    Calling percentOnBeatTaughtList on revised lanangPatterns, with eighth pattern
    having all single and first double strokes removed
    
    >>> import copy
    >>> lanangPatterns = fp.separatePatternsByDrum()[0]
    >>> lanangPatternsCopy = copy.deepcopy(lanangPatterns)
    >>> lanangPatternsCopy[7] = removedFirstDouble
    >>> lanangPatternsCopy[7]
    <bali.Taught Pak Tut Lanang Dasar 2:(_). e _ _ . e _ , _ _ . e T _ T _>
    >>> percentlist = taught_questions.percentOnBeatTaughtList(lanangPatternsCopy, 'e')
    >>> percentlist[7]
    100.0
    
    TODO: Leslie -- how to deal with across a repetition boundary
    '''
    newDrumPatternList = copy.deepcopy(pattern.strokes)
    for i in range(1, len(pattern.strokes) - 1):
        if removeFirst is True:
            if pattern.strokes[i] == pattern.strokes[i + 1] and pattern.strokes[i] == typeOfStroke:
                newDrumPatternList[i] = '.'
        if removeSecond is True:
            if (pattern.strokes[i] == pattern.strokes[i + 1] and pattern.strokes[i] == typeOfStroke) or pattern.strokes[i] == '.':
                newDrumPatternList[i+1] = '.'

    newDrumPattern = copy.deepcopy(pattern)
    newDrumPattern.strokes = newDrumPatternList
    
    return newDrumPattern


def percentOnBeatConsecutivesRemoved(pattern, typeOfStroke='e'):
    '''
    Returns percent of given stroke that occurs on the beat, only counting the second
    stroke of double strokes
    >>> import bali, taught_questions
    >>> fp = bali.FileParser()
    >>> pattern = fp.taught[25]
    >>> taught_questions.percentOnBeatConsecutivesRemoved(pattern, 'e')
    80.0
    '''
    
    patternConsecutivesRemoved = removeConsecutiveStrokes(pattern, typeOfStroke='e')
    patternStrokes = patternConsecutivesRemoved.strokes
    totalPercent = 0
    strokesCounted = 0
    strokesOfType = patternStrokes.count(typeOfStroke)
    strokesCounted += strokesOfType
    
    
    numberOnBeat = 0
    numberOfStroke = 0
    for i in range(len(patternStrokes)):
        if patternStrokes[i] not in typeOfStroke:
            continue
        numberOfStroke += 1
        if (i) % 2 == 0:
            numberOnBeat += 1

    if numberOfStroke == 0:
        return 0

    totalPercent += ((numberOnBeat * 100) / numberOfStroke) * strokesOfType
    if strokesCounted == 0:
        return 0
    return totalPercent / strokesCounted

# print(percentOnBeatConsecutivesRemoved(fp.taught[25], 'e'))

def percentOnBeatConsecutivesRemovedList(listOfPatterns, typeOfStroke='e'):
    '''
    Returns percent on beat for a certain type of stroke for every pattern in
    a list of patterns, with only the second stroke counted in double strokes.
    Organized as a dictionary with pattern as key and percent on beat as value
    
    >>> import bali, taught_questions
    >>> fp = bali.FileParser()
    >>> lanangPatterns = fp.separatePatternsByDrum()[0]
    >>> pakcok7 = lanangPatterns[-1]
    >>> pakcok7
    <bali.Taught Pak Cok Lanang 7 (not taught):(_)_ _ e e T _ _ _ e e T e T e T _>
    
    >>> outDict = taught_questions.percentOnBeatConsecutivesRemovedList(lanangPatterns, 'e')
    >>> outDict[pakcok7]
    100.0
    '''
    percents = {}
    for pattern in listOfPatterns:
        percent = percentOnBeatConsecutivesRemoved(pattern, typeOfStroke)
        percents[pattern] = percent
    return percents

# print(percentOnBeatConsecutivesRemovedList(lanangPatterns, 'e'))

def totalPercentOnBeatConsecutivesRemoved(listOfPatterns, typeOfStroke='e'):
    '''
    Returns percent on beat for a certain type of stroke for all patterns in
    a list of patterns, with only the second stroke counted in double strokes.
    '''
    percent = 0
    strokesCounted = 0
    patternDict = percentOnBeatConsecutivesRemovedList(listOfPatterns, typeOfStroke)
    for k in patternDict.keys():
        strokesOfType = k.drumPattern.count(typeOfStroke)
        strokesCounted += strokesOfType
        percent += patternDict[k] * strokesOfType
    return percent / strokesCounted
# print(totalPercentOnBeatConsecutivesRemoved(lanangPatterns, typeOfStroke='e'))

if __name__ == '__main__':
    import music21
    music21.mainTest()
    
  
