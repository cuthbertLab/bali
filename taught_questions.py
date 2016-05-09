# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

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

def percentOnBeatLanangE():
    '''
    Returns percent on beat for a lanang Peng for every pattern, at beat level double
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatLanangE()
    >>> len(percentList)
    41
    >>> percentList[1][0]
    85.7...
    >>> percentList[-1][0]
    66.6...
    
    >>> num = 0
    >>> denom = 0
    >>> for (percent, weight) in percentList:
    ...     num += percent * weight
    ...     denom += weight
    >>> num/denom
    56...
    '''
    lanangPatterns = fp.separatePatternsByDrum()[0]
    percents = []
    for i in range(len(lanangPatterns)):
        percent = lanangPatterns[i].percentOnBeat('e')
        weight = lanangPatterns[i].beatsInPattern('e')
        percents.append((percent, weight))
    return percents

def percentOffBeatLanangTGuntang():
    '''
    Returns percent off beat for a lanang 'T' stroke for every pattern, at beat level guntang
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOffBeatLanangTGuntang()
    >>> percentList[1][0]
    100.0
    >>> percentList[-1][0]
    100.0
    
    >>> num = 0
    >>> denom = 0
    >>> for (percent, weight) in percentList:
    ...     num += percent * weight
    ...     denom += weight
    >>> num/denom
    97...
    '''
    lanangPatterns = fp.separatePatternsByDrum()[0]
    percents = []
    for i in range(len(lanangPatterns)):
        pattern = lanangPatterns[i]
        percent = pattern.percentOnBeat('T', bali.BeatLevel.guntang)
        weight = pattern.beatsInPattern('T')
        percents.append((100 - percent, weight))
    return percents


def percentOffBeatLanangTDouble():
    '''
    Returns percent off beat for a lanang 'T' stroke for every pattern, at beat level double
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOffBeatLanangTDouble()
    >>> percentList[1][0]
    100.0
    >>> percentList[-1][0]
    100.0
    
    >>> num = 0
    >>> denom = 0
    >>> for (percent, weight) in percentList:
    ...     num += percent * weight
    ...     denom += weight
    >>> num/denom
    92...
    '''
    lanangPatterns = fp.separatePatternsByDrum()[0]
    percents = []
    for i in range(len(lanangPatterns)):
        pattern = lanangPatterns[i]
        percent = pattern.percentOnBeat('T', bali.BeatLevel.double)
        weight = pattern.beatsInPattern('T')
        percents.append((100 - percent, weight))
    return percents

#test Leslie's theory, make new tests for wadon, sparser beat levels, split and join patterns

def percentOffBeatWadonO():
    '''
    Returns percent of single 'o' strokes that land off the beat in wadon patterns

    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOffBeatWadonO()
    
    >>> num = 0
    >>> denom = 0
    >>> for (percent, weight) in percentList:
    ...     num += percent * weight
    ...     denom += weight
    >>> num/denom
    90...
    
    '''
    wadonPatterns = fp.separatePatternsByDrum()[1]
    percents = []
    for pattern in wadonPatterns:
        pattern = pattern.removeConsecutiveStrokes('o', removeSecond=True)
        percent = pattern.percentOnBeat('o')
        weight = pattern.beatsInPattern('o')
        percents.append((100 - percent, weight))
    return percents


def percentOnBeatWadonDGuntang():
    '''
    Returns percent on beat for a wadon 'D' for every pattern, at beat level guntang
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatWadonDGuntang()
    >>> percentList[4][0]
    33...
    >>> percentList[-1][0]
    33...
    
    >>> num = 0
    >>> denom = 0
    >>> for (percent, weight) in percentList:
    ...     num += percent * weight
    ...     denom += weight
    >>> num/denom
    26...
    '''
    wadonPatterns = fp.separatePatternsByDrum()[1]
    percents = []
    for i in range(len(wadonPatterns)):
        pattern = wadonPatterns[i]
        percent = pattern.percentOnBeat('D', bali.BeatLevel.guntang)
        weight = pattern.beatsInPattern('D')
        percents.append((percent, weight))
    return percents


def percentOnBeatWadonDDouble():
    '''
    Returns percent on beat for a wadon 'D' for every pattern, at beat level double
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatWadonDDouble()
    >>> percentList[4][0]
    100.0
    >>> percentList[-1][0]
    33...
    
    >>> num = 0
    >>> denom = 0
    >>> for (percent, weight) in percentList:
    ...     num += percent * weight
    ...     denom += weight
    >>> num/denom
    44.0
    '''
    wadonPatterns = fp.separatePatternsByDrum()[1]
    percents = []
    for i in range(len(wadonPatterns)):
        pattern = wadonPatterns[i]
        percent = pattern.percentOnBeat('D', bali.BeatLevel.double)
        weight = pattern.beatsInPattern('D')
        percents.append((percent, weight))
    return percents


if __name__ == '__main__':
    import music21
    music21.mainTest()
    
  
