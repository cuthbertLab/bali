# -*- coding: utf-8 -*-
'''
bali -- collection of modules for analyzing Balinese music

Copyright 2016, cuthbertLab at MIT

Released under the BSD 3-Clause license.


Authors: Katherine Young <kayoung@mit.edu>
         Michael Scott Cuthbert
'''
from __future__ import print_function, absolute_import, division

#import bali  
import io
import os 
import re
#import weakref
import unittest
import copy

import music21 # @UnresolvedImport

class BaliException(Exception):
    pass

class IncorrectBeatNumberException(BaliException):
    pass

class Pattern(object):
    '''
    Represents one drum pattern.

    >>> import bali
    >>> fp = bali.FileParser()
    >>> pattern = fp.taught[1]
    >>> pattern
    <bali.Taught Pak Tama Lanang 0 (intro):(_)_ _ e e _ e _ e _ e _ e _ e T _>    
    >>> pattern.title
    'Pak Tama Lanang 0 (intro)'
    >>> pattern.gongPattern
    '(4)- ● - 1 - ● - 2 - ● - 3 - ● – 4'
    >>> pattern.drumPattern
    '(_)_ _ e e _ e _ e _ e _ e _ e T _'
    >>> pattern.comments is None
    True
    >>> pattern.comments = 'intro pattern'
    >>> pattern.comments
    'intro pattern'
    >>> pattern.indexInFile
    1
    '''
    def __init__(self):
        self.title = ""
        self.gongPattern = ""
        self.drumPattern = ""
        self.comments = ""
        self.indexInFile = -1 # -1 means undefined. otherwise 0 to ...
        self.fileParser = None # the FileParser object.
      
    def copy(self):
        '''
        Returns a copy of the Pattern
        
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern
        <bali.Taught Pak Tama Lanang 0 (intro):(_)_ _ e e _ e _ e _ e _ e _ e T _>
        
        >>> pCopy = pattern.copy()
        >>> pCopy.title = 'wild lanang'
        >>> pCopy
        <bali.Taught wild lanang:(_)_ _ e e _ e _ e _ e _ e _ e T _>
        >>> pattern
        <bali.Taught Pak Tama Lanang 0 (intro):(_)_ _ e e _ e _ e _ e _ e _ e T _>
        
        '''  
        return copy.deepcopy(self)
      
    def _getStrokes(self):
        '''
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.strokes
        ['_', '_', '_', 'e', 'e', '_', 'e', '_', 'e', '_', 'e', '_', 'e', '_', 'e', 'T', '_']
        '''
        dp = self.drumPattern
        dpPreface = dp[0:3]
        beatZero = dpPreface[1]
        dpReal = dp[3:]
        postBeatZeroStrokes = dpReal.split()
        allStrokes = [beatZero] + postBeatZeroStrokes

        return allStrokes

    def _setStrokes(self, newStrokes):
        '''
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.drumPattern
        '(_)_ _ e e _ e _ e _ e _ e _ e T _'
        >>> st = pattern.strokes
        >>> st
        ['_', '_', '_', 'e', 'e', '_', 'e', '_', 'e', '_', 'e', '_', 'e', '_', 'e', 'T', '_']
        >>> st[1] = 'T'
        
        >>> import copy
        >>> patternCopy = copy.deepcopy(pattern)
        >>> patternCopy.strokes = st
        >>> patternCopy.drumPattern
        '(_)T _ e e _ e _ e _ e _ e _ e T _'

        Double check we did not change the original:
        
        >>> pattern.drumPattern
        '(_)_ _ e e _ e _ e _ e _ e _ e T _'
        >>> st = pattern.strokes
        >>> st
        ['_', '_', '_', 'e', 'e', '_', 'e', '_', 'e', '_', 'e', '_', 'e', '_', 'e', 'T', '_']
        
        '''
        beatZeroStroke = newStrokes[0]
        normalStrokes = newStrokes[1:]
        newDrumPatternNormalPart = ' '.join(normalStrokes)
        newDrumPatternAll = '(' + beatZeroStroke + ')' + newDrumPatternNormalPart
        self.drumPattern = newDrumPatternAll
        
    strokes = property(_getStrokes, _setStrokes, doc='''
        Gets or sets the list of Strokes.
    ''')

    def beatLength(self):
        '''
        The beatLength of a Pattern is defined as the last
        thing (hopefully a number) in the Gong Pattern.
       
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.gongPattern
        '(4)- ● - 1 - ● - 2 - ● - 3 - ● – 4'
        >>> pattern.beatLength()
        4
        >>> pattern.gongPattern = '(6)- ● - 1 - ● - 2 - ● - 3 - ● – 4 - ● – 5 - ● – 6'
        >>> pattern.beatLength()
        6
        '''
        gp = self.gongPattern
        lastLetter = gp[-1]
        lastNumber = int(lastLetter)
        return lastNumber
   
    def iterateStrokes(self, maxBeat=4.0):
        '''
        Use only in a for loop: goes through
        each stroke and tells you what the beat is
        and then what the stroke letter is.

        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> for beat, stroke in pattern.iterateStrokes(maxBeat=1.0):
        ...     print(beat, stroke)
        0.25 _
        0.5 _
        0.75 e
        1.0 e
        '''
        beat = 0.25
        strokeNumber = 1
        stroke = self.strokes
        while beat <= maxBeat:
            yield beat, stroke[strokeNumber]
            beat += 0.25
            strokeNumber += 1
    
    def typeOfStrokeByBeat(self, beat):
        '''
        Returns type of stroke on a given beat.

        >>> from music21 import *
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.typeOfStrokeByBeat(1)
        'e'
        >>> pattern.typeOfStrokeByBeat(3.75)
        'T'
        >>> pattern.typeOfStrokeByBeat(0.25)
        '_'
        '''
        return self.strokes[int(beat * 4)]
        
    def descriptionOfStroke(self, stroke):
        '''
        Returns description and type of the given stroke symbol.

        >>> from music21 import *
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.descriptionOfStroke('e')
        'Lanang high stroke'
        >>> pattern.descriptionOfStroke('T')
        'Lanang low stroke'
        >>> pattern.descriptionOfStroke('_')
        'ghost stroke'
        >>> pattern.descriptionOfStroke('aaa')
        Traceback (most recent call last):
        bali.BaliException: I do not know how to deal with this stroke
        '''
        
        strokeDict = {'e': 'Lanang high stroke',
                      'T': 'Lanang low stroke',
                      'd': 'Wadon stroke, quieter',
                      'D': 'Wadon bass stroke on big drum, louder',
                      'D.': 'dampened Wadon bass stroke on big drum',
                      'o': 'Wadon high stroke',
                      'L': 'left hand Wadon stroke', #not supposed to be there, lowercase l
                      '_': 'ghost stroke',
                      'r': 'right hand ghost stroke',
                      'l': 'left hand ghost stroke',
                      'G': 'gong stroke',
                      'pu': 'pung stroke',
                      '?': 'unclear stroke',
                      'U': 'taking and giving cue for dancer/singer/end of line in Lanang',
                      'C': 'right hand pitched stroke',
                      '-': 'beat in gong, metronome',
                      'P': 'left hand slap stroke',
                      'n': 'kempyang',
                      't': 'guntang',
                      'K': 'left hand slap stroke on Wadon',
                      '`': 'nothing'}

        if stroke in strokeDict:
            return strokeDict[stroke]
        else:
            raise BaliException('I do not know how to deal with this stroke')


        unused_strokeNames = {'e': 'peng',
                      'T': 'tut', # doot
                      'd': 'dit',
                      'D': 'dag', #or deg
                      'D.': '', #
                      'o': 'kom',
                      'L': 'left hand Wadon stroke', #not supposed to be there, lowercase l
                      '_': 'ghost stroke',
                      'r': 'right hand ghost stroke',
                      'l': 'left hand ghost stroke',
                      'G': 'gong stroke',
                      'pu': 'pung stroke',
                      '?': 'unclear stroke',
                      'U': 'taking and giving cue for dancer/singer/end of line in Lanang',
                      'C': 'right hand pitched stroke',
                      '-': 'beat in gong, metronome',
                      'P': 'left hand slap stroke',
                      'n': 'kempyang',
                      't': 'guntang',
                      'K': 'left hand slap stroke on Wadon',
                      '`': 'nothing'}

    def consecutiveStrokes(self):
        '''
        Finds all consecutive patterns (like oo) and returns copy of pattern
        with repeated strokes removed and only final stroke shown, with
        repeated strokes replaced by '.'
        Example: Pak Tama Lanang 0 (intro) should return
        ['_', '_', '_', '.', 'e', '_', 'e', '_', 'e', '_', 'e', '_', 'e', '_', 'e', 'T', '_']

        >>> from music21 import *
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.title
        'Pak Tama Lanang 0 (intro)'
        >>> pattern.drumPattern
        '(_)_ _ e e _ e _ e _ e _ e _ e T _'
        
        >>> pattern.consecutiveStrokes()
        ['_', '_', '_', '.', 'e', '_', 'e', '_', 'e', '_', 'e', '_', 'e', '_', 'e', 'T', '_']
        '''
        consecutiveStrokesRemoved = self.strokes
        repeatedStrokes = []
        for stroke in range(1, len(self.strokes) - 1):
            if self.strokes[stroke] != '_' and stroke < len(self.strokes) - 1:
                if self.strokes[stroke] == self.strokes[stroke + 1]:              
                    repeatedStrokes.append(self.strokes[stroke])
                    consecutiveStrokesRemoved[stroke] = '.'
        return consecutiveStrokesRemoved

    def isValidBeat(self, beat):
        '''
        Checks if beat entered is a valid beat in Taught Patterns.
        If not, prompts user to enter a valid beat.

        >>> from music21 import *
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.isValidBeat(3.2)
        Please enter an integer from 1-4
        False
        >>> pattern.isValidBeat("hii")
        Please enter an integer from 1-4
        False
        >>> pattern.isValidBeat(6)
        Please enter an integer from 1-4
        False
        >>> pattern.gongPattern = '(6)- ● - 1 - ● - 2 - ● - 3 - ● – 4 - ● – 5 - ● – 6'
        >>> pattern.beatLength()
        6
        >>> pattern.isValidBeat(5)
        True
        >>> pattern.isValidBeat(7)
        Please enter an integer from 1-6
        False
        '''
        if beat not in range(1, self.beatLength()) or beat != int(beat):
            print("Please enter an integer from 1-" + str(self.beatLength()))
            return False
        else:
            return True

    def allLeadingUpToBeat(self, beatLedUpTo):
        '''
        Finds everything leading up to certain beat and places them in
        allLeadingUpToBeat.
        Example: Pak Tama Lanang 0 (intro) should return
        ['_', '_', 'e', 'e'] for leading up to beat 1.
        
        >>> from music21 import *
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.allLeadingUpToBeat(1)
        ['_', '_', 'e', 'e']        
        '''
        if self.isValidBeat(beatLedUpTo):
            allLeadingUpToBeat = []
            for i in range(4 * beatLedUpTo - 3,
                           4 * beatLedUpTo + 1):
                allLeadingUpToBeat.append(self.strokes[i])
            return allLeadingUpToBeat
        else:
            raise IncorrectBeatNumberException("Wrong beat")

    def strokesLeadingUpToBeat(self, beatLedUpTo):
        '''
        Finds all strokes that aren't '_' leading up to certain beat and places them in
        strokesLeadingUpToBeat.
        Example: Pak Tama Lanang 0 (intro) should return
        ['e', 'e'] for leading up to beat 1.

        >>> from music21 import *
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.strokesLeadingUpToBeat(1)
        ['e', 'e']        
        '''
        if self.isValidBeat(beatLedUpTo):
            strokesLeadingUpToBeat = []
            for i in range((4 * beatLedUpTo) - 3,
                           (4 * beatLedUpTo) + 1):
                if self.strokes[i] != '_':
                    strokesLeadingUpToBeat.append(self.strokes[i])
            return strokesLeadingUpToBeat
        else:
            raise IncorrectBeatNumberException("Wrong beat")
            

    def contiguousStrokesLeadingUpToBeat(self, beatLedUpTo):
        '''
        Finds all strokes that aren't '_' and are contiguous leading up to certain beat
        and places them in contiguousLeadingUpToBeat.
        Example: Pak Dewa Lanang 10 should return
        ['e', 'e', 'T'] for leading up to beat 1.
        
        >>> from music21 import *
        >>> import bali
        >>> fp = bali.FileParser()
        
        >>> pattern = fp.taught[4]
        >>> pattern
        <bali.Taught Pak Dewa Lanang 10:(_)e e T e _ _ _ _ e e _ e _ e _ _>
        
        >>> pattern.contiguousStrokesLeadingUpToBeat(1)
        ['e', 'e', 'T']
        >>> pattern.contiguousStrokesLeadingUpToBeat(2)
        []
        '''
        if self.isValidBeat(beatLedUpTo):
            contiguousStrokesLeadingUpToBeat = []
            for i in range(4 * beatLedUpTo - 1,
                           4 * beatLedUpTo - 4,
                           -1):
                if self.strokes[i] == '_':
                    break
                else:
                    contiguousStrokesLeadingUpToBeat.insert(0, self.strokes[i])
            return contiguousStrokesLeadingUpToBeat
        else:
            raise IncorrectBeatNumberException("Wrong beat")

    def sameStrokesLeadingUpToBeat(self, beatLedUpTo):
        '''
        Finds all strokes leading up to certain beat that are the same
        as that stroke and places them in sameStrokesLeadingUpToBeat.
        Example: Pak Tama Lanang 0 (intro) should return
        ['e'] for leading up to beat 1.
        Example 2: Pak Dewa Lanang 10 should return
        [] for leading up to beat 1.
        
        >>> from music21 import *
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.sameStrokesLeadingUpToBeat(1)
        ['e']        
        >>> pattern = fp.taught[4]
        >>> pattern.sameStrokesLeadingUpToBeat(1)
        [] 
        '''
        if self.isValidBeat(beatLedUpTo):
            sameStrokesLeadingUpToBeat = []
            for i in range(4 * beatLedUpTo,
                           4 * beatLedUpTo - 4,
                           -1):
                if self.strokes[i] == '_' or self.strokes[i-1] != self.strokes[i]:
                    break
                elif self.strokes[i-1] == self.strokes[i] and self.strokes[i-1] != '_':
                    sameStrokesLeadingUpToBeat.insert(0, self.strokes[i-1])
            return sameStrokesLeadingUpToBeat
        else:
            raise IncorrectBeatNumberException("Wrong beat")
        
    def percentOnBeat(self, typeOfStroke='e'):
        '''
        Returns percent of a certain type of stroke that occurs on the beat
        Helper function for percentOnBeatTaught
        
        >>> import bali, taught_questions
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.percentOnBeat('e')
        85.7...
        
        >>> pattern2 = fp.taught[-1]
        >>> pattern.percentOnBeat('o')
        0.0
        
        >>> pattern.percentOnBeat('T')
        0.0
        '''
        numberOnBeat = 0
        numberOfStroke = 0
        for beat, stroke in self.iterateStrokes():
            if stroke != typeOfStroke:
                continue
            numberOfStroke += 1
            if (beat * 2) % 1 == 0:
                numberOnBeat += 1
    
        if numberOfStroke == 0:
            return 0.0
        return (numberOnBeat * 100) / numberOfStroke

    def percentOnBeatTaught(self, typeOfStroke='e'):
        '''
        Returns percent of a certain type of stroke that occurs on the beat
        Double counts end and beginning of each pattern
        
        >>> import bali, taught_questions
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.percentOnBeatTaught('e')
        85.7...
        '''
        totalPercent = 0
        strokesCounted = 0
        strokesOfType = self.drumPattern.count(typeOfStroke)
        strokesCounted += strokesOfType
        totalPercent += self.percentOnBeat(typeOfStroke) * strokesOfType
        if strokesCounted == 0:
            return 0.0
        return totalPercent / strokesCounted

    def removeSingleStrokes(self, typeOfStroke='e'):
        '''
        Returns drum pattern with all single strokes of a given type removed
        The single strokes are replaced with ','
    
        >>> import bali, taught_questions
        >>> fp = bali.FileParser()
        
        >>> pattern = fp.taught[4]
        >>> pattern
        <bali.Taught Pak Dewa Lanang 10:(_)e e T e _ _ _ _ e e _ e _ e _ _>
        >>> removed = pattern.removeSingleStrokes('e')
        >>> removed
        <bali.Taught Pak Dewa Lanang 10:(_)e e T , _ _ _ _ e e _ , _ , _ _>
        >>> removed.percentOnBeatTaught('e')
        50.0
        
        >>> pattern2 = fp.taught[-1]
        >>> pattern2
        <bali.Taught Pak Tama Wadon Variant 3:(_)o o D _ _ _ o o D _ d D _ _ o _>
        >>> removed2 = pattern2.removeSingleStrokes('D')
        >>> removed2
        <bali.Taught Pak Tama Wadon Variant 3:(_)o o , _ _ _ o o , _ d , _ _ o _>
        >>> removed3 = pattern2.removeSingleStrokes('o')
        >>> removed3
        <bali.Taught Pak Tama Wadon Variant 3:(_)o o D _ _ _ o o D _ d D _ _ , _>
        >>> removed3.percentOnBeatTaught('o')
        50.0
        '''
        newDrumPatternList = copy.deepcopy(self.strokes)
        for i in range(1, len(self.strokes) - 1):
            if self.strokes[i] != self.strokes[i + 1] and self.strokes[i] == typeOfStroke:
                if self.strokes[i - 1] != typeOfStroke:
                    newDrumPatternList[i] = ','
                    
        newDrumPattern = copy.deepcopy(self)
        newDrumPattern.strokes = newDrumPatternList
        
        return newDrumPattern
        
    def removeConsecutiveStrokes(self, typeOfStroke='e', removeFirst=True, removeSecond=False):
        '''
        Returns drum pattern with first stroke of a double stroke of a given type removed.
        
        The first stroke of a double stroke is replaced with '.'
        
        >>> import bali, taught_questions
        >>> fp = bali.FileParser()
        >>> lanang10 = fp.taught[4]
        >>> lanang10
        <bali.Taught Pak Dewa Lanang 10:(_)e e T e _ _ _ _ e e _ e _ e _ _>
        
        >>> removed = lanang10.removeConsecutiveStrokes('e')
        >>> removed
        <bali.Taught Pak Dewa Lanang 10:(_). e T e _ _ _ _ . e _ e _ e _ _>
        >>> removed.percentOnBeatTaught('e')
        100.0
        >>> lanang10
        <bali.Taught Pak Dewa Lanang 10:(_)e e T e _ _ _ _ e e _ e _ e _ _>
    
        >>> removed2 = lanang10.removeConsecutiveStrokes('e', removeSecond=True)
        >>> removed2
        <bali.Taught Pak Dewa Lanang 10:(_). . T e _ _ _ _ . . _ e _ e _ _>
        >>> lanang10
        <bali.Taught Pak Dewa Lanang 10:(_)e e T e _ _ _ _ e e _ e _ e _ _>
    
    
        Not appearing in the repertoire except by mistake, but for completeness sake
        the name of this method is correct.  It removes all but the last even
        in cases where there are three or more in a row, unless removeSecond is True
    
        >>> screwedUpLanang = fp.taught[4].copy()
        >>> screwedUpLanang.drumPattern = '(_)e e T e _ _ _ _ e e e _ _ e _ _'
        >>> removed = screwedUpLanang.removeConsecutiveStrokes('e')
        >>> removed
        <bali.Taught Pak Dewa Lanang 10:(_). e T e _ _ _ _ . . e _ _ e _ _>
        
        
        Testing removing single strokes first, then removing first double strokes
        
        >>> pattern2 = fp.taught[7]
        >>> pattern2
        <bali.Taught Pak Tut Lanang Dasar 2:(_)e e _ _ e e _ e _ _ e e T _ T _>
        
        >>> removedSingle = pattern2.removeSingleStrokes('e')
        >>> removedSingle
        <bali.Taught Pak Tut Lanang Dasar 2:(_)e e _ _ e e _ , _ _ e e T _ T _>
        
        >>> removedSingle.percentOnBeatTaught('e')
        50.0
        
        >>> removedFirstDouble = removedSingle.removeConsecutiveStrokes('e')
        >>> removedFirstDouble
        <bali.Taught Pak Tut Lanang Dasar 2:(_). e _ _ . e _ , _ _ . e T _ T _>
        >>> removedFirstDouble.percentOnBeatTaught('e')
        100.0
        
        
        Testing removing both double strokes (removeFirst is True by default)
        
        >>> removedSingle
         <bali.Taught Pak Tut Lanang Dasar 2:(_)e e _ _ e e _ , _ _ e e T _ T _>
        >>> removedBothDoubles = removedSingle.removeConsecutiveStrokes('e', removeSecond=True)
        >>> removedBothDoubles
        <bali.Taught Pak Tut Lanang Dasar 2:(_). . _ _ . . _ , _ _ . . T _ T _>
        
        Calling percentOnBeatTaughtList on revised lanangPatterns, with eighth pattern
        having all single and first double strokes removed
        
        >>> import statistics
        >>> lanangPatterns = fp.separatePatternsByDrum()[0]
        >>> numLanang = len(lanangPatterns)
        
        >>> percentListBefore = taught_questions.percentOnBeatTaughtList(lanangPatterns, 'e')
        >>> percentListBefore[7]
        57...
        >>> statistics.mean(percentListBefore)
        54...

        >>> for i in range(numLanang):
        ...     lanangPatterns[i] = lanangPatterns[i].removeConsecutiveStrokes('e')
        >>> lanangPatterns[7]
        <bali.Taught Pak Tut Lanang Dasar 2:(_). e _ _ . e _ e _ _ . e T _ T _>
        
        >>> percentListAfter = taught_questions.percentOnBeatTaughtList(lanangPatterns, 'e')
        >>> percentListAfter[7]
        100.0
        >>> statistics.mean(percentListAfter)
        80.0
        
        
        
        TODO: Leslie -- how to deal with across a repetition boundary
        '''
        newDrumPatternList = copy.deepcopy(self.strokes)
        for i in range(1, len(self.strokes) - 1):
            if removeFirst is True:
                if self.strokes[i] == self.strokes[i + 1] and self.strokes[i] == typeOfStroke:
                    newDrumPatternList[i] = '.'
            if removeSecond is True:
                if (self.strokes[i] == self.strokes[i + 1] and self.strokes[i] == typeOfStroke) or self.strokes[i] == '.':
                    newDrumPatternList[i+1] = '.'
    
        newDrumPattern = copy.deepcopy(self)
        newDrumPattern.strokes = newDrumPatternList
        
        return newDrumPattern


    def __repr__(self):
        return '<{0}.{1} {2}:{3}>'.format(self.__module__, self.__class__.__name__,
                                          self.title, self.drumPattern)

        
class FileParser(object):
    '''
    Reads both files on disk (FileReader) and separates them into taught and transcribed patterns.
    '''
    def __init__(self):
        self.fileReader = FileReader()
        #time.sleep(1)
        self.taughtPatterns = []
        self.transcribedPatterns = []

    @property
    def taught(self):
        if len(self.taughtPatterns) > 0:
            return self.taughtPatterns
        else:
            self.parseTaught(self.fileReader.taught)
            return self.taughtPatterns

    def separatePatternsByDrum(self):
        lanangPatterns = []
        wadonPatterns = []
        for p in self.taught:
            if p.drumType == 'Lanang':
                lanangPatterns.append(p)
            elif p.drumType == 'Wadon':
                wadonPatterns.append(p)
        return lanangPatterns, wadonPatterns

    @property
    def transcribed(self):
        if self.transcribedPatterns:
            return self.transcribedPatterns
        else:
            self.parseTranscribed(self.fileReader.transcribed)
            return self.transcribedPatterns

    def parseTaught(self, lineList):
        '''
        Takes a list of lines from a file and an empty list [] and fills that
        list with Taught objects.
        
        >>> import bali
        >>> fp = bali.FileParser()
        >>> lineList = fp.taught
        >>> lineList[4]
        <bali.Taught Pak Dewa Lanang 10:(_)e e T e _ _ _ _ e e _ e _ e _ _>
        '''
        currentTitle = None
        currentGongPattern = None
        currentDrumPattern = None
        currentComments = None
        currentPatternIndex = 0
        
        for line in lineList:
            if line == '' and currentTitle is None:
                continue
            elif line == '':
                patt = Taught()
                patt.indexInFile = currentPatternIndex
                currentPatternIndex += 1
                patt.fileParser = self
                
                if currentTitle.endswith(':'):
                    currentTitle = currentTitle[0:len(currentTitle) - 1]
                patt.title = currentTitle
                patt.gongPattern = currentGongPattern
                patt.drumPattern = currentDrumPattern
                patt.comments = currentComments
                self.taughtPatterns.append(patt)
                currentTitle = None
                currentGongPattern = None
                currentDrumPattern = None
                currentComments = None
            elif currentTitle is None:
                currentTitle = line
            elif currentGongPattern is None:
                currentGongPattern = line
            elif currentDrumPattern is None:
                currentDrumPattern = line
            else:
                currentComments = line
        
    def parseTranscribed(self, lineList):
        '''
        Takes a list of lines from a file and an empty list [] and fills that
        list with Pattern objects.

        This is not a good way to do this for later.
        '''
        currentTitle = ""
        currentGongPattern = None
        currentDrumPattern = None
        currentComments = None
        currentPatternIndex = 0
        
        for line in lineList:
            if line == '' and currentTitle is None:
                continue
            elif line == '':
                patt = Transcribed()
                patt.indexInFile = currentPatternIndex
                currentPatternIndex += 1
                patt.fileParser = self
                
                if currentTitle.endswith(':'):
                    currentTitle = currentTitle[0:len(currentTitle) - 1]
                patt.title = currentTitle
                patt.gongPattern = currentGongPattern
                patt.drumPattern = currentDrumPattern
                patt.comments = currentComments
                self.transcribedPatterns.append(patt)
                currentTitle = None
                currentGongPattern = None
                currentDrumPattern = None
                currentComments = None
            elif currentTitle is None:
                currentTitle = line
            elif currentGongPattern is None:
                currentGongPattern = line
            elif currentDrumPattern is None:
                currentDrumPattern = line
            else:
                currentComments = line

class FileReader(object):
    def __init__(self):
        self.directory = os.path.dirname(__file__)
        self._taught = os.path.join(self.directory, 'taught_patterns.txt')
        self._transcribed = os.path.join(self.directory, 'all_patterns.txt')
        self._taughtContents = None
        self._transcribedContents = None

    @property
    def taught(self):
        if self._taughtContents is not None:
            return self._taughtContents
        with io.open(self._taught, encoding='utf-8') as t:
            self._taughtContents = t.readlines()
        
        for i in range(len(self._taughtContents)):
            self._taughtContents[i] = self._taughtContents[i].strip()
        return self._taughtContents
    
    @property
    def transcribed(self):
        if self._transcribedContents is not None:
            return self._transcribedContents
        with io.open(self._transcribed, encoding='utf-8') as t:
            self._transcribedContents = t.readlines()
        for i in range(len(self._transcribedContents)):
            self._transcribedContents[i] = self._transcribedContents[i].strip()

        return self._transcribedContents
     
class Taught(Pattern):
    @property
    def drumType(self):
        '''
        Get the teacher's name from the taught pattern

        >>> from music21 import *
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.drumType
        'Lanang'
        '''
        if 'lanang' in self.title.lower():
            return 'Lanang'
        elif 'wadon' in self.title.lower():
            return 'Wadon'
        else:
            return 'unknown'
        
    @property
    def teacher(self):
        '''
        Get the teacher's name from the taught pattern

        >>> from music21 import *
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.taught[1]
        >>> pattern.teacher
        'Pak Tama'
        '''
        if 'Sudi' in self.title:
            return 'Sudi'
        m = re.match(r'(Pak\s\w+)\s', self.title)
        if m is not None:
            return m.group(1)
                      
class Transcribed(Pattern):
    def drumTypeInfer(self):
        '''
        Infers type of drum from strokes for transcribed patterns

        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.transcribed[4]
        >>> pattern.drumTypeInfer()
        'Lanang'

        >>> pattern = fp.transcribed[110]
        
        <<< pattern.drumTypeInfer()
        'Wadon'
        '''
        if self.drumPattern is None:
            raise BaliException("Cannot infer drum type when drumPattern is None")
            
        if any(x in self.drumPattern for x in ['e', 'T', 'U']):
            return 'Lanang'
        if any(x in self.drumPattern for x in ['d', 'D', 'D.', 'o', 'K']):
            return 'Wadon'
        else:
            return 'unknown'
    
    def timeAtBeat(self, patternIndex, beat):
        '''
        Extracts time at a certain beat, given in 00:00:00 = minute:second:centisecond,
        extrapolated from time at beginning of current pattern and beginning of next
        pattern. Only works for patterns with timings at beginning

        >>> from music21 import *
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.transcribed[4]
        >>> pattern.timeAtBeat(4, 2)
        '0:0:8.75'
        '''
        fp = FileParser()
        pointInPattern = (len(self.strokes[:beat * 2 * 2])) / (len(self.strokes) - 1)
        timeFirstPattern = fp.transcribed[patternIndex].title.split(':')
        timeNextPattern = fp.transcribed[patternIndex + 1].title.split(':')
        centisecondsFirstPattern = (timeFirstPattern[0] * 6000 + timeFirstPattern[1] * 100
                                    + timeFirstPattern[2])
        centisecondsNextPattern = (timeNextPattern[0] * 6000 + timeNextPattern[1] * 100
                                   + timeNextPattern[2])
        deltaCentiseconds = pointInPattern * (int(centisecondsNextPattern) - 
                                                int(centisecondsFirstPattern))
        newInCentiseconds = int(centisecondsFirstPattern) + deltaCentiseconds
        newMinutes = int(newInCentiseconds / 6000)
        newSeconds = int((newInCentiseconds - newMinutes * 6000) / 100)
        newCentiseconds = newInCentiseconds - newMinutes * 6000 - newSeconds * 100
        time = ':'.join([str(newMinutes), str(newSeconds), str(newCentiseconds)])
        return time

    def lastBeatOfLastPattern(self):
        '''
        Finds stroke of last beat of preceding pattern.

        Does not work for patterns with two drummers
        
        >>> from music21 import *
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.transcribed[5]
        >>> pattern.lastBeatOfLastPattern()
        'r'       
        '''
        for index in range(len(self.drumPattern)):
            if self.drumPattern[index] == '(':
                if self.drumPattern[index + 2] == ')':
                    return self.drumPattern[index + 1]
            else:
                return self.strokes[0]
            
class PatternHolder():
    '''
    a class of objects that hold multiple patterns or things that hold multiple patterns.
    allows multiple patterns to be combined and to get next/previous pattern

    Maybe we will need this? maybe not...
    '''
    pass

class Session(PatternHolder):
    def __init__(self):
        self.subsessionsByPlayer = []
        self.nameOfPlayers = ""
        self.indexInFile = -1
        self.parentFileParser = None

    def nextSession(self):
        '''
        Gets next session 
        '''
        pass

    def previousSession(self):
        '''
        Gets previous session 
        '''
        pass

    def combineWithNextSession(self):
        '''
        Combines current session object with next session object.
        '''
    
class SubsessionByPlayer(PatternHolder):
    def __init__(self):
        self.improvsInGong = []
        self.indexInSession = -1
        self.isSinglePlayer = True
        self.drumType = "" # lanang, wadon, or both...
        self.lanangPlayerName = ""
        self.wadonPlayerName = ""
        self.parentSubsession = None

    def nextSubsessionByPlayer(self):
        '''
        Gets next subsession by player
        '''
        pass

    def previousSubsessionByPlayer(self):
        '''
        Gets previous subsession by player
        '''
        pass

    def combineWithNextSubsessionByPlayer(self):
        '''
        Combines current subsession object with next subsession object.
        '''
        
class ImprovInGong(PatternHolder):
    def __init__(self):
        self.typeOfGong = ""
        self.indexInSubsessionByPlayer = -1
        self.patterns = []
        self.parentSubsessionByPlayer = None

    def nextImprovInGong(self):
        '''
        Gets next pattern. 
        
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.transcribed[4]
        
        xxx pattern.nextImprovInGong()
        <bali.Pattern 00:00:11:(r)l l T r e e T r e e T r e e T e T r e e r e T r l r T r U _ T l>
        '''
        try:
            fp = self.fileParser
            currentIndex = self.indexInFile
            return fp.transcribed[currentIndex + 1]
        except IndexError:
            return None

    def previousImprovInGong(self):
        '''
        Gets previous pattern.
        
        >>> import bali
        >>> fp = bali.FileParser()
        >>> pattern = fp.transcribed[5]
        >>> pattern.previousImprovInGong()
        <bali.Pattern 00:00:08:(r)l r e e T e T e T e T e T e T e T e T e T e T r e e T e T e T r>
        '''
        fp = self.fileParser
        currentIndex = self.indexInFile
        if currentIndex != 0:
            return fp.transcribed[currentIndex - 1]
        else:
            return None

    def combineWithNextImprovInGong(self):
        '''
        Combines current pattern object with next pattern object. 
        not sure how to combine into new pattern object
        '''
        fp = FileParser()
        currentIndex = fp.transcribed.index(self)
        try:
            return self, fp.transcribed[currentIndex + 1]
        except IndexError: 
            return self

    def nextTimePoint(self):
        '''
        Gets next time point in transcribed patterns
        '''
        pass

    def improv(self):
        '''
        Gets name of improv of current pattern
        Go back to previous == and return that string
        '''
        pass

class SingleDrummer(PatternHolder):
    def __init__(self):
        self.typeOfGong = ""
        self.indexInSubsessionByPlayer = -1
        self.patterns = []
        self.parentSubsessionByPlayer = None

class DualDrummer(PatternHolder):
    def __init__(self):
        self.typeOfGong = ""
        self.indexInSubsessionByPlayer = -1
        self.patterns = []
        self.parentSubsessionByPlayer = None

    def firstDrummerPattern(self):
        pass
    
    def secondDrummerPattern(self):
        pass
        

###### Tests

class Test(unittest.TestCase):
    def testWhyDoesFirstTaughtFail(self):
        import bali
        
        fp = bali.FileParser()
        pattern = fp.taught[0]
        self.assertEqual(''.join(pattern.drumPattern), '(e)_ e _ e _ e _ e _ e _ e _ e _ e')
    
        # make sure we end with Wadon variant 3
        lastPattern = fp.taught[-1]
        self.assertEqual(lastPattern.title, 'Pak Tama Wadon Variant 3')
    
    def xtestDrumTypeInfer(self):
        import bali
        
        fp = bali.FileParser()
        pattern = fp.transcribed[110]
        drumTypeInferred = pattern.drumTypeInfer()
        
        self.assertEqual(drumTypeInferred, 'Wadon')

if __name__ == '__main__':
    music21.mainTest(Test)
