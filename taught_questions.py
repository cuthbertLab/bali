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

def percentOnBeat(pattern, typeOfStroke='e'):
    '''
    Returns percent of a certain type of stroke that occurs on the beat
    Helper function for percentOnBeatTaught
    
    >>> import bali, taught_questions
    >>> fp = bali.FileParser()
    >>> pattern = fp.taught[1]
    >>> taught_questions.percentOnBeat(pattern, 'e')
    85.7...
    '''
    numberOnBeat = 0
    numberOfStroke = 0
    for beat, stroke in pattern.iterateStrokes():
        if stroke != typeOfStroke:
            continue
        numberOfStroke += 1
        if (beat * 2) % 1 == 0:
            numberOnBeat += 1

    if numberOfStroke == 0:
        return 0
    return (numberOnBeat * 100) / numberOfStroke
#print(percentOnBeat(fp.taught[1], 'e'))

def percentOnBeatTaught(pattern, typeOfStroke='e'):
    '''
    Returns percent of a certain type of stroke that occurs on the beat
    Double counts end and beginning of each pattern
    
    >>> import bali, taught_questions
    >>> fp = bali.FileParser()
    >>> pattern = fp.taught[1]
    >>> taught_questions.percentOnBeatTaught(pattern, 'e')
    85.7...
    '''
    totalPercent = 0
    strokesCounted = 0
    strokesOfType = pattern.drumPattern.count(typeOfStroke)
    strokesCounted += strokesOfType
    totalPercent += percentOnBeat(pattern, typeOfStroke) * strokesOfType
    if strokesCounted == 0:
        return 0
    return totalPercent / strokesCounted
#print(percentOnBeatTaught(fp.taught[1], 'e'))

def percentOnBeatTaughtList(listOfPatterns, typeOfStroke='e'):
    '''
    Returns percent on beat for a certain type of stroke for every pattern in
    a list of patterns. Organized as a dictionary with pattern as key and 
    percent on beat as value
    
    >>> import bali, taught_questions
    >>> fp = bali.FileParser()
    >>> lanangPatterns = fp.separatePatternsByDrum()[0]
    >>> returnedDict = taught_questions.percentOnBeatTaughtList(lanangPatterns, 'e')
    >>> returnedDict['(l)_ e _ l _ e _ l _ e _ l _ e T l']
    100.0
    '''
    percents = {}
    for pattern in listOfPatterns:
        percent = percentOnBeatTaught(pattern, typeOfStroke)
        percents[pattern.drumPattern] = percent
    return percents

# lanangPatterns = []
# wadonPatterns = []
# for p in fp.taught:
#     if p.drumType == 'Lanang':
#         lanangPatterns.append(p)
#     elif p.drumType == 'Wadon':
#         wadonPatterns.append(p)
# print(percentOnBeatTaughtList(lanangPatterns, 'e'))

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
    >>> taught_questions.percentOnBeatTaught(removed, 'e')
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
    >>> taught_questions.percentOnBeatTaught(removed, 'e')
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
    
    >>> removedsingle = taught_questions.removeSingleStrokes(pattern2, 'e')
    >>> removedsingle
    <bali.Taught Pak Tut Lanang Dasar 2:(_)e e _ _ e e _ , _ _ e e T _ T _>
    
    >>> taught_questions.percentOnBeatTaught(removedsingle, 'e')
    50.0
    
    >>> removedfirstdouble = taught_questions.removeConsecutiveStrokes(removedsingle, 'e')
    >>> removedfirstdouble
    <bali.Taught Pak Tut Lanang Dasar 2:(_). e _ _ . e _ , _ _ . e T _ T _>
    >>> taught_questions.percentOnBeatTaught(removedfirstdouble, 'e')
    100.0
    
    >>> removedbothdoubles = taught_questions.removeConsecutiveStrokes(removedsingle, 'e', removeSecond=True)
    >>> removedbothdoubles
    <bali.Taught Pak Tut Lanang Dasar 2:(_). . _ _ . . _ , _ _ . . T _ T _>
    
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
    
  
