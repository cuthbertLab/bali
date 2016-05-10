# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division

#from pprint import pprint as print
import bali, itertools
fp = bali.FileParser()

class PercentList(list):
    '''
    A list where each element is a tuple of (percent, weight), that
    can calculate certain things...
    '''

    def num(self):
        '''
        return the numerator of the weighted mean
        '''
        tot = 0
        for percent, weight in self:
            tot += percent * weight
        return tot

    def denom(self):
        '''
        return the total amount of weight in the list 
        '''
        tot = 0
        for unused_percent, weight in self:
            tot += weight
        return tot

    def weighedTotalPercentage(self):
        '''
        return num/denom...
        '''
        denom = self.denom()
        if denom == 0:
            raise ZeroDivisionError("There are no matching strokes in this list") 
        return self.num()/denom

'''
What percentage of Lanang is on the beat with nothing changed?
'''

def percentOnBeatLanangEDouble():
    '''
    Returns a PercentList for a lanang peng for every pattern, at beat level double
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatLanangEDouble()
    >>> len(percentList)
    41
    >>> percentList[1][0]
    85.7...
    >>> percentList[-1][0]
    66.6...
    >>> percentList.weighedTotalPercentage()
    56.8...
    '''
    lanangPatterns = fp.separatePatternsByDrum()[0]
    percents = PercentList()
    for pattern in lanangPatterns:
        percent = pattern.percentOnBeat('e')
        weight = pattern.beatsInPattern('e')
        percents.append((percent, weight))
    return percents


'''
Testing that peng strokes occur on the beat in lanang and kom strokes occur off
the beat in wadon, after removing all double strokes. 
'''

def percentOnBeatLanangEDoubleSingle():
    '''
    Returns PercentList for on-beats for peng strokes for all lanang patterns, 
    at beat level double
    Only looks at single strokes
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatLanangEDoubleSingle()
    
    >>> percentList[1][0]
    100.0
    >>> percentList[4][0]
    100.0
    
    >>> percentList.weighedTotalPercentage()
    68.7...
    >>> percentList.denom()
    96.0
    '''
    lanangPatterns = fp.separatePatternsByDrum()[0]
    percents = PercentList()
    for pattern in lanangPatterns:
        pattern = pattern.removeConsecutiveStrokes('e', True, True)
        percent = pattern.percentOnBeat('e', bali.BeatLevel.double)
        weight = pattern.beatsInPattern('e')
        percents.append((percent, weight))
    return percents


def percentOffBeatWadonODoubleSingle():
    '''
    Returns PercentList for off-beats for kom strokes for all wadon patterns, 
    at beat level double
    Only looks at single strokes

    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOffBeatWadonODoubleSingle()
    
    >>> percentList[1][0]
    100.0
    >>> percentList[5][0]
    75.0
    
    >>> percentList.weighedTotalPercentage()
    90.7...
    >>> percentList.denom()
    65

    '''
    wadonPatterns = fp.separatePatternsByDrum()[1]
    percents = PercentList()
    for pattern in wadonPatterns:
        pattern = pattern.removeConsecutiveStrokes('o', True, True)
        percent = pattern.percentOnBeat('o', bali.BeatLevel.double)
        weight = pattern.beatsInPattern('o')
        percents.append((100 - percent, weight))
    return percents


'''
Testing that lanang peng strokes are off the beat and wadon kom strokes are on the
beat when single and the first of all double strokes are removed, at beat level guntang
'''

def percentOffBeatLanangEGuntangSecondDouble():
    '''
    Returns PercentList for off-beats for a peng for all lanang patterns, at beat level guntang,
    after removing single strokes and then first of consecutive strokes
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOffBeatLanangEGuntangSecondDouble()
    >>> percentList[1][0]
    0.0
    >>> percentList[4][0]
    100.0
    
    >>> percentList.weighedTotalPercentage()
    75.9...
    >>> percentList.denom()
    83.0
    '''
    lanangPatterns = fp.separatePatternsByDrum()[0]
    percents = PercentList()
    for pattern in lanangPatterns:
        pattern = pattern.removeSingleStrokes('e')
        pattern = pattern.removeConsecutiveStrokes('e')
        percent = pattern.percentOnBeat('e', bali.BeatLevel.guntang)
        weight = pattern.beatsInPattern('e')
        percents.append((100 - percent, weight))
    return percents


def percentOnBeatWadonOGuntangSecondDouble():
    '''
    Returns PercentList for on-beats for a kom for all wadon pattern, at beat level guntang,
    after removing all single strokes and the first of all double strokes
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatWadonOGuntangSecondDouble()
    >>> percentList[8][0]
    100.0
    >>> percentList[-1][0]
    50.0
    
    >>> percentList.weighedTotalPercentage()
    62.0...
    >>> percentList.denom()
    29.0
    '''
    wadonPatterns = fp.separatePatternsByDrum()[1]
    percents = PercentList()
    for pattern in wadonPatterns:
        pattern = pattern.removeSingleStrokes('o')
        pattern = pattern.removeConsecutiveStrokes('o')
        percent = pattern.percentOnBeat('o', bali.BeatLevel.guntang)
        weight = pattern.beatsInPattern('o')
        percents.append((percent, weight))
    return percents


'''
Dag and tut strokes

Normally, lanang tuts are off the beat and wadon dags are on the beat. 
Wadon breaks the rules more, so we are testing in which beat subdivisions
and part of the gong cycle the rules are broken more
'''

def percentOffBeatLanangTGuntang():
    '''
    Returns PercentList for off-beats for a lanang tut strokes for all lanang patterns, 
    at beat level guntang. 
    
    Gives us what percent tut strokes land on beat subdivisions 1 and 3 as opposed to
    2 and 4
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOffBeatLanangTGuntang()
    >>> percentList[1][0]
    100.0
    >>> percentList[-1][0]
    100.0
    
    >>> percentList.weighedTotalPercentage()
    97.2...
    >>> percentList.denom()
    111.0
    '''
    lanangPatterns = fp.separatePatternsByDrum()[0]
    percents = PercentList()
    for pattern in lanangPatterns:
        percent = pattern.percentOnBeat('T', bali.BeatLevel.guntang)
        weight = pattern.beatsInPattern('T')
        percents.append((100 - percent, weight))
    return percents


def percentOnBeatWadonDGuntang():
    '''
    Returns PercentList for on-beats for dag strokes for all wadon patterns, 
    at beat level guntang. 
    First of all double strokes removed.
    Gives us what percent dag strokes land on beat subdivisions 2 and 4 as opposed to
    1 and 3
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatWadonDGuntang()
    >>> percentList[4][0]
    33.3...
    >>> percentList[-3][0]
    50.0
    
    >>> percentList.weighedTotalPercentage()
    26.0
    >>> percentList.denom()
    50.0
    
    Great confirmation of a null hypothesis: 25%
    '''
    
    wadonPatterns = fp.separatePatternsByDrum()[1]
    percents = PercentList()
    for pattern in wadonPatterns:
        pattern = pattern.removeConsecutiveStrokes('Dd')
        percent = pattern.percentOnBeat('D', bali.BeatLevel.guntang)
        weight = pattern.beatsInPattern('D')
        percents.append((percent, weight))
    return percents


def whenLanangOffTList(beatDivision='first'):
    '''
    Returns distribution of which half of the gong lanang tuts land in
    when they're on the first or third division of the beat
    In dictionary form.
    
    >>> import bali, taught_questions
    
    Testing when beatDivision is first
    
    >>> taught_questions.whenLanangOffTList()['first half']
    5
    >>> taught_questions.whenLanangOffTList()['second half']
    20
    
    
    Testing when beatDivision is third
    
    >>> taught_questions.whenLanangOffTList('third')['first half']
    27
    >>> taught_questions.whenLanangOffTList('third')['second half']
    51
    '''
    
    lanangPatterns = fp.separatePatternsByDrum()[0]
    dist = {'first half': 0, 'second half': 0}
    if beatDivision == 'first':
        for pattern in lanangPatterns:
            dist['first half'] += pattern.whenLanangOffT()['first half']
            dist['second half'] += pattern.whenLanangOffT()['second half']
    elif beatDivision == 'third':
        for pattern in lanangPatterns:
            dist['first half'] += pattern.whenLanangOffT('third')['first half']
            dist['second half'] += pattern.whenLanangOffT('third')['second half']        
    return dist 



def whenWadonOffDList(beatDivision='first'):
    '''
    Returns distribution of which half of the gong wadon dags land in
    when they're on the first or third division of the beat. 
    In dictionary form.
    
    >>> import bali, taught_questions
    
    Testing when beatDivision is first
    
    >>> taught_questions.whenWadonOffDList()['first half']
    17
    >>> taught_questions.whenWadonOffDList()['second half']
    11
    
    
    Testing when beatDivision is third
    
    >>> taught_questions.whenWadonOffDList('third')['first half']
    6
    >>> taught_questions.whenWadonOffDList('third')['second half']
    1
    '''
    
    wadonPatterns = fp.separatePatternsByDrum()[1]
    dist = {'first half': 0, 'second half': 0}
    if beatDivision == 'first':
        for pattern in wadonPatterns:
            dist['first half'] += pattern.whenWadonOffD()['first half']
            dist['second half'] += pattern.whenWadonOffD()['second half']
    elif beatDivision == 'third':
        for pattern in wadonPatterns:
            dist['first half'] += pattern.whenWadonOffD('third')['first half']
            dist['second half'] += pattern.whenWadonOffD('third')['second half']
    return dist 


'''
Testing if Leslie's theories are statistically significant (p < 0.05), using
randomly generated scrambled drum patterns 
'''

def createRandomPatterns(numberOfPatterns):
    '''
    Returns a list of numberOfPattern Pattern objects whose strokes are scrambled randomly
    
    >>> import bali, taught_questions, itertools
    >>> fp = bali.FileParser()


    Creating shuffled list of length 4
    
    >>> randomList4 = taught_questions.createRandomPatterns(4)
    >>> len(randomList4)
    4
    >>> pattern = randomList4[0]
    >>> pattern.drumPattern.count('e')
    9
    
    
    Creating shuffled list of length 100
    
    >>> randomList100 = taught_questions.createRandomPatterns(100)
    >>> len(randomList100)
    100
    >>> pattern2 = randomList100[3]
    >>> pattern2.strokes.count('e')
    7
    >>> ''.join(pattern2.strokes).count('T')
    1
    
    Checking that itertools.cycle looped around correctly
    >>> pattern3 = randomList100[63]
    >>> pattern3.strokes.count('e')
    9
    >>> pattern3.strokes.count('T')
    0
    '''
    
    fp = bali.FileParser()
    taughtPatterns = [patt for patt in fp.taught]
    
    randomPatterns = itertools.cycle(taughtPatterns)
    randomPatternsList = []
    count = 0
    for pattern in randomPatterns:
        randomPatternsList.append(pattern.shuffleStrokes())
        count += 1
        if count >= numberOfPatterns:
            break
    return randomPatternsList
        
'''
Testing all the above theories with scrambled patterns
'''

'''
What percentage of Lanang is on the beat with nothing changed? With scrambled strokes?
'''

def percentOnBeatLanangEDoubleScrambled():
    '''
    Returns a PercentList for a lanang peng for every pattern, at beat level double
    With scrambled strokes
    If a certain scrambled pattern beat the theory, it was added to beatTheory
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatLanangEDoubleScrambled()[0]
    >>> beatTheory = taught_questions.percentOnBeatLanangEDoubleScrambled()[1]
    >>> percentList.weighedTotalPercentage() < 58.6
    True
    
    >>> len(beatTheory) < 40
    True 
    
    #also a bad threshold
  
    '''
    randomPatterns = createRandomPatterns(100)
    percents = PercentList()
    beatTheory = []
    for pattern in randomPatterns:
        if pattern.drumType == 'Lanang':
            percent = pattern.percentOnBeat('e')
            weight = pattern.beatsInPattern('e')
            if percent >= 58.6:
                beatTheory.append(pattern.drumPattern)
            percents.append((percent, weight))
    return (percents, beatTheory)


'''
Testing that peng strokes occur on the beat in lanang and kom strokes occur off
the beat in wadon, after removing all double strokes. With scrambled patterns.
'''

def percentOnBeatLanangEDoubleSingleScrambled():
    '''
    Returns PercentList for on-beats for peng strokes for all lanang patterns, 
    at beat level double
    Only looks at single strokes
    With scrambled strokes. 
    If a certain scrambled pattern beat the theory, it was added to beatTheory
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatLanangEDoubleSingleScrambled()[0]
    >>> beatTheory = taught_questions.percentOnBeatLanangEDoubleSingleScrambled()[1]
    >>> percentList.weighedTotalPercentage() < 68.7
    True
    
    >>> len(beatTheory) < 25
    True
    
    #bad threshold
    '''
    randomPatterns = createRandomPatterns(100)
    percents = PercentList()
    beatTheory = []
    for pattern in randomPatterns:
        if pattern.drumType == 'Lanang':
            pattern = pattern.removeConsecutiveStrokes('e', True, True)
            percent = pattern.percentOnBeat('e', bali.BeatLevel.double)
            weight = pattern.beatsInPattern('e')
            if percent >= 68.7:
                beatTheory.append(pattern.drumPattern)
            percents.append((percent, weight)) 
    return (percents, beatTheory)


def percentOffBeatWadonODoubleSingleScrambled():
    '''
    Returns PercentList for off-beats for kom strokes for all wadon patterns, 
    at beat level double
    Only looks at single strokes
    With scrambled strokes
    If a certain scrambled pattern beat the theory, it was added to beatTheory

    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOffBeatWadonODoubleSingleScrambled()[0]
    >>> beatTheory = taught_questions.percentOffBeatWadonODoubleSingleScrambled()[1]
    >>> percentList.weighedTotalPercentage() < 90.7
    True

    >>> len(beatTheory) < 10
    True
    '''
    randomPatterns = createRandomPatterns(100)
    percents = PercentList()
    beatTheory = []
    for pattern in randomPatterns:
        if pattern.drumType == 'Wadon':
            pattern = pattern.removeConsecutiveStrokes('o', True, True)
            percent = pattern.percentOnBeat('o', bali.BeatLevel.double)
            weight = pattern.beatsInPattern('o')
            if percent < 9.3:
                beatTheory.append(pattern.drumPattern)
            percents.append((100 - percent, weight))
    return (percents, beatTheory)


'''
Testing that lanang peng strokes are off the beat and wadon kom strokes are on the
beat when single and the first of all double strokes are removed, at beat level guntang
'''

def percentOffBeatLanangEGuntangSecondDoubleScrambled():
    '''
    Returns PercentList for off-beats for a peng for all lanang patterns, at beat level guntang,
    after removing single strokes and then first of consecutive strokes
    With scrambled strokes
    If a certain scrambled pattern beat the theory, it was added to beatTheory
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOffBeatLanangEGuntangSecondDoubleScrambled()[0]
    >>> beatTheory = taught_questions.percentOffBeatLanangEGuntangSecondDoubleScrambled()[1]
    >>> percentList.weighedTotalPercentage() < 75.9
    True
    
    >>> len(beatTheory) < 10
    True

    '''
    randomPatterns = createRandomPatterns(100)
    percents = PercentList()
    beatTheory = []
    for pattern in randomPatterns:
        if pattern.drumType == 'Lanang':
            pattern = pattern.removeSingleStrokes('e')
            pattern = pattern.removeConsecutiveStrokes('e')
            percent = pattern.percentOnBeat('e', bali.BeatLevel.guntang)
            weight = pattern.beatsInPattern('e')
            if percent > 75.9:
                beatTheory.append(pattern.drumPattern)
            percents.append((100 - percent, weight))
    return (percents, beatTheory)


def percentOnBeatWadonOGuntangSecondDoubleScrambled():
    '''
    Returns PercentList for on-beats for a kom for all wadon pattern, at beat level guntang,
    after removing all single strokes and the first of all double strokes
    With scrambled strokes
    If a certain scrambled pattern beat the theory, it was added to beatTheory
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatWadonOGuntangSecondDoubleScrambled()[0]
    >>> beatTheory = taught_questions.percentOnBeatWadonOGuntangSecondDoubleScrambled()[1]
    >>> percentList.weighedTotalPercentage() < 62
    True
    
    >>> len(beatTheory) < 30
    True
    
    #this is a low threshold
    '''
    randomPatterns = createRandomPatterns(100)
    percents = PercentList()
    beatTheory = []
    for pattern in randomPatterns:
        if pattern.drumType == 'Wadon':
            pattern = pattern.removeSingleStrokes('o')
            pattern = pattern.removeConsecutiveStrokes('o')
            percent = pattern.percentOnBeat('o', bali.BeatLevel.guntang)
            weight = pattern.beatsInPattern('o')
            if percent >= 62:
                beatTheory.append(pattern.drumPattern)
            percents.append((percent, weight))
    return (percents, beatTheory)

'''
Dag and tut strokes

Normally, lanang tuts are off the beat and wadon dags are on the beat. 
Wadon breaks the rules more, so we are testing in which beat subdivisions
and part of the gong cycle the rules are broken more
'''

def percentOffBeatLanangTGuntangScrambled():
    '''
    Returns PercentList for off-beats for a lanang tut strokes for all lanang patterns, 
    at beat level guntang. 
    With scrambled strokes
    If a certain scrambled pattern beat the theory, it was added to beatTheory
    
    Gives us what percent tut strokes land on beat subdivisions 1 and 3 as opposed to
    2 and 4
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOffBeatLanangTGuntangScrambled()[0]
    >>> beatTheory = taught_questions.percentOffBeatLanangTGuntangScrambled()[1]
    >>> percentList.weighedTotalPercentage() < 97.2
    True

    >>> len(beatTheory) < 10
    True
    '''
    randomPatterns = createRandomPatterns(100)
    percents = PercentList()
    beatTheory = []
    for pattern in randomPatterns:
        if pattern.drumType == 'Lanang':
            percent = pattern.percentOnBeat('T', bali.BeatLevel.guntang)
            weight = pattern.beatsInPattern('T')
            if percent < 2.8:
                beatTheory.append(pattern.drumPattern)
            percents.append((100 - percent, weight))
    return (percents, beatTheory)


def percentOnBeatWadonDGuntangScrambled():
    '''
    Returns PercentList for on-beats for dag strokes for all wadon patterns, 
    at beat level guntang. 
    First of all double strokes removed.
    Gives us what percent dag strokes land on beat subdivisions 2 and 4 as opposed to
    1 and 3
    With scrambled strokes
    If a certain scrambled pattern beat the theory, it was added to beatTheory
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatWadonDGuntangScrambled()[0]
    >>> beatTheory = taught_questions.percentOnBeatWadonDGuntangScrambled()[1]
    >>> percentList.weighedTotalPercentage() < 30
    True
    
    >>> len(beatTheory) < 20
    True
    '''
    
    randomPatterns = createRandomPatterns(100)
    percents = PercentList()
    beatTheory = []
    for pattern in randomPatterns:
        if pattern.drumType == 'Wadon':
            pattern = pattern.removeConsecutiveStrokes('Dd')
            percent = pattern.percentOnBeat('D', bali.BeatLevel.guntang)
            weight = pattern.beatsInPattern('D')
            if percent >= 26:
                beatTheory.append(pattern.drumPattern)
            percents.append((percent, weight))
    return (percents, beatTheory)


def whenLanangOffTListScrambled(beatDivision='first'):
    '''
    Returns distribution of which half of the gong lanang tuts land in
    when they're on the first or third division of the beat
    In dictionary form.
    With scrambled strokes
    
    >>> import bali, taught_questions
    
    Testing when beatDivision is first
    
    >>> (taught_questions.whenLanangOffTListScrambled()['first half']) / (taught_questions.whenLanangOffTListScrambled()['second half'])
    
    
    Testing when beatDivision is third
    
    >>> (taught_questions.whenLanangOffTListScrambled('third')['first half']) / (taught_questions.whenLanangOffTListScrambled('third')['second half'])

    '''
    
    randomPatterns = createRandomPatterns(100)
    dist = {'first half': 0, 'second half': 0}
    if beatDivision == 'first':
        for pattern in randomPatterns:
            if pattern.drumType == 'Lanang':
                dist['first half'] += pattern.whenLanangOffT()['first half']
                dist['second half'] += pattern.whenLanangOffT()['second half']
    elif beatDivision == 'third':
        for pattern in randomPatterns:
            if pattern.drumType == 'Lanang':
                dist['first half'] += pattern.whenLanangOffT('third')['first half']
                dist['second half'] += pattern.whenLanangOffT('third')['second half']        
    return dist 



def whenWadonOffDListScrambled(beatDivision='first'):
    '''
    Returns distribution of which half of the gong wadon dags land in
    when they're on the first or third division of the beat. 
    In dictionary form.
    With scrambled strokes
    
    >>> import bali, taught_questions
    
    Testing when beatDivision is first
    
    >>> (taught_questions.whenWadonOffDListScrambled()['first half']) / (taught_questions.whenWadonOffDListScrambled()['second half'])

    
    Testing when beatDivision is third
    
    >>> (taught_questions.whenWadonOffDListScrambled('third')['first half']) / (taught_questions.whenWadonOffDListScrambled('third')['second half'])

    '''
    
    randomPatterns = createRandomPatterns(100)
    dist = {'first half': 0, 'second half': 0}
    if beatDivision == 'first':
        for pattern in randomPatterns:
            if pattern.drumType == 'Wadon':
                dist['first half'] += pattern.whenWadonOffD()['first half']
                dist['second half'] += pattern.whenWadonOffD()['second half']
    elif beatDivision == 'third':
        for pattern in randomPatterns:
            if pattern.drumType == 'Wadon':
                dist['first half'] += pattern.whenWadonOffD('third')['first half']
                dist['second half'] += pattern.whenWadonOffD('third')['second half']
    return dist 




'''   
Miscellaneous tests not necessarily in Leslie's theories
'''
    
def percentOffBeatLanangTDouble():
    '''
    Returns PercentList for off-beats for a tut strokes for all lanang patterns, 
    at beat level double.
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOffBeatLanangTDouble()
    >>> percentList[1][0]
    100.0
    >>> percentList[-1][0]
    100.0
    
    >>> percentList.weighedTotalPercentage()
    92.7...
    >>> percentList.denom()
    111.0
    '''
    lanangPatterns = fp.separatePatternsByDrum()[0]
    percents = PercentList()
    for i in range(len(lanangPatterns)):
        pattern = lanangPatterns[i]
        percent = pattern.percentOnBeat('T', bali.BeatLevel.double)
        weight = pattern.beatsInPattern('T')
        percents.append((100 - percent, weight))
    return percents


def percentOnBeatWadonDDouble():
    '''
    Returns percent on beat for a wadon 'D' for every pattern, at beat level double
    
    >>> import bali, taught_questions
    >>> percentList = taught_questions.percentOnBeatWadonDDouble()
    >>> percentList[4][0]
    100.0
    >>> percentList[-1][0]
    33.3...
    
    >>> percentList.weighedTotalPercentage()
    44.0
    >>> percentList.denom()
    50.0
    
    Close to null hypothesis
    '''
    wadonPatterns = fp.separatePatternsByDrum()[1]
    percents = PercentList()
    for i in range(len(wadonPatterns)):
        pattern = wadonPatterns[i]
        percent = pattern.percentOnBeat('D', bali.BeatLevel.double)
        weight = pattern.beatsInPattern('D')
        percents.append((percent, weight))
    return percents


if __name__ == '__main__':
    import music21
    music21.mainTest()
    
  
