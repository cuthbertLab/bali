from __future__ import print_function, division

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

lanangPatterns = []
wadonPatterns = []
for p in fp.taught:
    if p.drumType == 'Lanang':
        lanangPatterns.append(p)
    elif p.drumType == 'Wadon':
        wadonPatterns.append(p)

lan = lanangPatterns[0:10]
wad = wadonPatterns[0:22]

def percentOnBeat(pattern, typeOfStroke = 'e'):
    '''
    Returns percent of a certain type of stroke that occurs on the beat
    Helper function for percentOnBeatTaught
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

def percentOnBeatTaught(pattern, typeOfStroke = 'e'):
    '''
    Returns percent of a certain type of stroke that occurs on the beat
    Double counts end and beginning of each pattern
    >>> from music21 import *
    >>> import bali
    >>> fp = bali.FileParser()
    >>> pattern = fp.taught[0]
    >>> percentOnBeatTaught(pattern, 'e')
    100
    '''
    totalPercent = 0
    strokesCounted = 0
    strokesOfType = pattern.drumPattern.count(typeOfStroke)
    strokesCounted += strokesOfType
    totalPercent += percentOnBeat(pattern, typeOfStroke) * strokesOfType
    if strokesCounted == 0:
        return 0
    return totalPercent / strokesCounted

print('percentOnBeatTaught Lanang')
print(percentOnBeatTaught(lan, 'e'))
print('percentOnBeatTaught Wadon')
print(percentOnBeatTaught(wad, 'o'))

def percentOnBeatTaughtList(listOfPatterns, typeOfStroke = 'e'):
    '''
    Returns percent on beat for a certain type of stroke for every pattern in
    a list of patterns. Organized as a dictionary with pattern as key and 
    percent on beat as value
    '''
    percents = {}
    for pattern in listOfPatterns:
        percent = percentOnBeatTaught(pattern, typeOfStroke)
        percents[pattern] = percent
    return percents
'''
Figure out if this "Lanang on beat, Wadon off beat" hypothesis doesn't hold with double strokes
'''

def separateSingleConsecutiveStrokes(listOfPatterns, typeOfStroke = 'e'):
    '''
    Separates patterns that only have single strokes from those with consecutive strokes
    Returns percent of a certain type of stroke that occurs on the beat for these two types
    of patterns
    Should handle triple/quadruple strokes (doesn't occur in taught)
    '''
    singleStrokePatterns = []
    doubleStrokePatterns = []
    for pattern in listOfPatterns:
        doubleStrokes = 0
        strokes = list(pattern.drumPattern.replace(' ', ''))
        for i in range(len(strokes) - 1):
            if strokes[i] == strokes[i + 1] and strokes[i] != '_':
                doubleStrokes += 1
        if doubleStrokes > 0:
            doubleStrokePatterns.append(pattern)
        else:
            singleStrokePatterns.append(pattern)
            
    percentOnBeatSingle = percentOnBeatTaught(singleStrokePatterns, typeOfStroke)
    percentOnBeatDouble = percentOnBeatTaught(doubleStrokePatterns, typeOfStroke)
    
    return ('Patterns with only single strokes:', singleStrokePatterns, percentOnBeatSingle,
           'Patterns with consecutive strokes', doubleStrokePatterns, percentOnBeatDouble)

print('separateSingleConsecutiveStrokes Lanang')
print(separateSingleConsecutiveStrokes(lan, 'e'))
print('separateSingleConsecutiveStrokes Wadon')
print(separateSingleConsecutiveStrokes(wad, 'o'))

'''
Take out double strokes of a certain type
'''

def removeDoubleStrokes(pattern, typeOfStroke = 'e'):
    '''
    Returns list of drum patterns (as lists) with first stroke of a double stroke of a given type removed.
    Should handle triple/quadruple strokes (don't occur in taught patterns)
    Doesn't return new pattern objects
    
    The first stroke of a double stroke is replaced with '.'
    >>> from music21 import *
    >>> import bali
    >>> fp = bali.FileParser()
    >>> pattern = fp.taught[0]
    >>> allRemoved = removeDoubleStrokes(pattern, 'e')
    >>> type(allRemoved) is list
    True
    >>> len(allRemoved)
    2
    >>> firstRemoved = allRemoved[0]
    >>> ''.join(firstRemoved)
    'e_e_e_e_e_e_e_e_e'
    '''
    strokesWithConsecutivesRemoved = []
    newDrumPattern = pattern.strokes
    for i in range(1, len(pattern.strokes) - 1):
        if pattern.strokes[i] == pattern.strokes[i + 1] and pattern.strokes[i] == typeOfStroke:
            newDrumPattern[i] = '.'
    strokesWithConsecutivesRemoved.append(newDrumPattern)
    return strokesWithConsecutivesRemoved

def percentOnBeatDoublesRemoved(pattern, typeOfStroke = 'e'):
    patternDoublesRemoved = removeDoubleStrokes(pattern, typeOfStroke = 'e')
    percent = percentOnBeatTaught(patternDoublesRemoved, typeOfStroke = 'e')
    return percent

def percentOnBeatDoublesRemovedList(listOfPatterns, typeOfStroke = 'e'):
    '''
    Returns percent on beat for a certain type of stroke for every pattern in
    a list of patterns, with only the second stroke counted in double strokes.
    Organized as a dictionary with pattern as key and percent on beat as value
    '''
    percents = {}
    for pattern in listOfPatterns:
        percent = percentOnBeatDoublesRemoved(pattern, typeOfStroke)
        percents[pattern] = percent
    return percents
    
print('removeDoubleStrokes Lanang')
print(removeDoubleStrokes(lan, 'e'))
print('removeDoubleStrokes Wadon')
print(removeDoubleStrokes(wad, 'o'))

if __name__ == '__main__':
    import sys
    sys.path.append('/Users/Katherine1/git/music21/')
    import music21
    music21.mainTest()
