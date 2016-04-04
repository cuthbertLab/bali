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

def percentOnBeat(listOfPatterns, typeOfStroke = 'e'):
    '''
    Returns percent of a certain type of stroke that occurs on the beat
    Helper function for percentOnBeatTaught
    '''
    numberOnBeat = 0
    numberOfStroke = 0
    for beat, stroke in listOfPatterns.iterateStrokes():
        if stroke != typeOfStroke:
            continue
        numberOfStroke += 1
        if (beat * 2) % 1 == 0:
            numberOnBeat += 1

    if numberOfStroke == 0:
        return 0
    return (numberOnBeat * 100) / numberOfStroke

def percentOnBeatTaught(listOfPatterns, typeOfStroke = 'e'):
    '''
    Returns percent of a certain type of stroke that occurs on the beat

    Double counts end and beginning of each pattern

    >>> from music21 import *
    >>> import bali
    >>> fp = bali.FileParser()
    >>> pattern = lanangPatterns[0:2]
    >>> percentOnBeatTaught(pattern, 'e')
    93.75
    '''
    global lanangPatterns, wadonPatterns

    totalPercent = 0
    strokesCounted = 0
    for pattern in listOfPatterns:
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

def removeDoubleStrokes(listOfPatterns, typeOfStroke = 'e'):
    '''
    Returns list of drum patterns (as lists) with first stroke of a double stroke of a given type removed.
    Should handle triple/quadruple strokes (don't occur in taught patterns)
    Doesn't return new pattern objects
    
    The first stroke of a double stroke is replaced with '.'
    >>> from music21 import *
    >>> import bali
    >>> fp = bali.FileParser()
    >>> pattern = lanangPatterns[0:2]
    >>> removeDoubleStrokes(pattern, 'e')
    [['e',
      '_',
      'e',
      '_',
      'e',
      '_',
      'e',
      '_',
      'e',
      '_',
      'e',
      '_',
      'e',
      '_',
      'e',
      '_',
      'e'],
     ['_',
      '_',
      '_',
      '.',
      'e',
      '_',
      'e',
      '_',
      'e',
      '_',
      'e',
      '_',
      'e',
      '_',
      'e',
      'T',
      '_']]
    '''
    strokesWithConsecutivesRemoved = []
    for pattern in listOfPatterns:
        newDrumPattern = pattern.strokes
        repeatedStrokes = []
        for i in range(1, len(pattern.strokes) - 1):
            if pattern.strokes[i] == pattern.strokes[i + 1] and pattern.strokes[i] == typeOfStroke:
                newDrumPattern[i] = '.'
        strokesWithConsecutivesRemoved.append(newDrumPattern)
    return strokesWithConsecutivesRemoved

print('removeDoubleStrokes Lanang')
print(removeDoubleStrokes(lan, 'e'))
print('removeDoubleStrokes Wadon')
print(removeDoubleStrokes(wad, 'o'))
   
if __name__ == '__main__':
    import sys
    sys.path.append('/Users/Katherine1/git/music21/')
    import music21
    music21.mainTest()
