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
    Returns percent on beat for a lanang Peng for every pattern.
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatLanangE()
    >>> len(percentList)
    41
    >>> percentList[1]
    85.7...
    >>> percentList[-1]
    66.6...
    '''
    lanangPatterns = fp.separatePatternsByDrum()[0]
    percents = []
    for i in range(len(lanangPatterns)):
        percents.append(lanangPatterns[i].percentOnBeat('e'))
    return percents

def percentOffBeatWadonO():
    '''
    Returns percent of single 'o' strokes that land off the beat in wadon patterns, 
    after all doubles strokes have been removed.

    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOffBeatWadonO()
    >>> percentList
    '''
    wadonPatterns = fp.separatePatternsByDrum()[1]
    percents = []
    for pattern in wadonPatterns:
        pattern = pattern.removeConsecutiveStrokes('o', removeSecond=True)
        thisNum = pattern.percentOnBeat('o')
        percents.append(100 - thisNum)
    return percents

def weighedPercentOffBeatWadonO():
    '''
    Returns percent of single 'o' strokes that land off the beat in wadon patterns, 
    after all doubles strokes have been removed.
    '''
    


'''
Figure out if this "Lanang on beat, Wadon off beat" hypothesis doesn't hold with double strokes
'''


if __name__ == '__main__':
    import music21
    music21.mainTest()
    
  
