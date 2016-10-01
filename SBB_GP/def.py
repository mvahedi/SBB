# Fall-Winter 2016 
__author__ = 'Maryam Vahedi'
###############################################################
###CLASSES
###############################################################
from config import *

class instruction:
    def __init__(self,mode,target,opcode,source, encoded):
        self.mode = mode
        self.target = target
        self.opcode = opcode
        self.source = source
        self.encoded = str(encoded)

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.encoded == other.encoded)

    def __ne__(self, other):
        return not self.__eq__(other)     

    def getMode(self):
        return self.mode

    def setMode(self, mode):
        self.mode = mode  
    
    def getTarget(self):
        return self.target

    def setTarget(self, target):
        self.target = target

    def getOpcode(self):
        return self.opcode

    def setOpcode(self, opcode):
        self.opcode = opcode

    def getSource(self):
        return self.source

    def setSource(self, source):
        self.source = source

    def getEncoded(self):
        return self.encoded

    def setEncoded(self, encoded):
        self.encoded = encoded

    def run_instruction(self, *args):
        #Target - First Source
        target = Decimal(args[0][0])
        if math.isinf(target):
            target = 0
        if self.getMode() == 0:
            #Attributes
            source = Decimal(args[1][int(self.getSource())])
        else:
            #Second Source
            source = Decimal(args[0][1]) 
        opcode = OPERATORS[int(self.getOpcode())]
        if opcode == '+':    
            target = Decimal(target) + Decimal(source)
        elif opcode == '-':
            target = Decimal(target) - Decimal(source)
        elif opcode == '*':
            try:
                target = Decimal(target) * Decimal(source)
            except:
                #print 'Math error Multiply'
                pass    
        elif opcode == '/':
            if source != 0:
                target = Decimal(target) / Decimal(source)
        elif opcode == 'cos':
            if source > 0:
                try:
                    target = Decimal(math.cos(Decimal(source)))
                except:
                    #print 'Math error COS'
                    pass    
        elif opcode == 'ln':
            try:
                if source > 0:
                    target = Decimal(math.log(Decimal(source), 2))  
            except:
                #print 'Math error LOG'
                pass    
        elif opcode == 'exp': 
            try:
                target = Decimal(math.exp(Decimal(source)))
            except:
                #print 'source: ', source, 'target: ', target
                #print 'Math error EXP'
                pass    
        elif opcode == 'if':
            if target < source:
                target = -Decimal(target)   
        args[0][self.getTarget()] = target
        return args[0]                        

    def print_instruction(self):
        print('Instruction mode: ' + str(self.getMode()) + ' target: ' + str(self.getTarget()) + ' opcode: ' + str(self.getOpcode()) + ' source: ' + str(self.getSource()) + " encoded: " + self.getEncoded())

class symbiont:
    def reset(self):
        self.bid = 0
        self.targetValues = []
        self.correctLabelCount = 0
        self.detection_rate = Decimal(0)
        for index in range(TARGET_COUNT):
            self.setTargetValue(0)  

    def evaluate(self, exemplar):
        tvs =  flatten(self.getTargetValues())
        for s in flatten(self.getInstructions()):
            if type(s) is list:
                for wtf in s:
                    tvs = wtf.run_instruction(flatten(tvs), exemplar)
            else:
                tvs = s.run_instruction(flatten(tvs), exemplar)
            self.targetValues = flatten(tvs)          
        self.bid = self.getTargetValues()[0] 

    def evaluateSymbiont(self):
        self.reset()
        for exemplar in data:
            self.evaluate(exemplar)       

    def __init__(self, instructions, action):
        self.instructions = []
        self.instructions = instructions[:]
        self.reset()
        self.action = action
        
    def __eq__(self, other):
        is_equal = False
        if isinstance(other, self.__class__):
            if self.bid == other.bid:
                is_equal = True;
                for ss in self.instructions:
                    exists = False
                    for os in other.instructions:
                        if ss == os:
                            exists = True
                            break
                    if not exists:
                        is_equal = False
                        break;        
        return is_equal 

    def __ne__(self, other):
        return not self.__eq__(other) 

    def __cmp__(self,other):
        return cmp(self.bid,other.bid)

    def getInstructions(self):
        return self.instructions

    def setInstructions(self, instructions):
        self.instructions = instructions  

    def getBid(self):
        return self.bid

    def setBid(self, bid):
        self.targetValues = bid   

    def getAction(self):
        return self.action 

    def setAction(self, action):
        self.action = action      

    def getTargetValues(self):
        return self.targetValues

    def setTargetValues(self, *targetValues):
        self.targetValues = targetValues

    def setTargetValue(self, targetValue):
        self.targetValues.append(targetValue) 

    def getCorrectLabelCount(self):
        return self.correctLabelCount

    def setCorrectLabelCount(self, correctLabelCount):
        self.correctLabelCount = correctLabelCount 

    def getDetectionRate(self):
        return self.detection_rate    

class team:
    def evaluate_team(self, exemplar):
        isCorrect = False
        for symbiont in self.symbionts:
            symbiont.reset()
            symbiont.evaluate(exemplar)    
        self.symbionts.sort(key = lambda i: i.getBid(), reverse=True)
        self.action = self.symbionts[0].getAction()
        if LABELS[self.action] == exemplar[LABEL_INDEX]:
            self.updateActiveSymbionts()
            isCorrect = True
            self.correct_count[self.action] = self.correct_count[self.action] + 1    
        return isCorrect

    def calculateDetectionRates(self, isTest = False, isAll = False):
        detectionRate = 0
        accumulativeDetectionRate = 0
        index = 0
        max_detected_value = None
        if isTest == True:
            ld = test_label_disctribution
        elif isAll == True:
            ld = label_disctribution   
        else:
            ld = train_label_disctribution
        while index < LABEL_COUNT:
            detected_value = Decimal(Decimal(self.correct_count[index]) / Decimal(ld[index]))
            if max_detected_value is None or max_detected_value < detected_value:
                max_detected_value = detected_value
                self.action = index
            detectionRate = detectionRate + Decimal(Decimal(self.correct_count[index]) / Decimal(ld[index]))
            accumulativeDetectionRate = accumulativeDetectionRate + Decimal(Decimal(self.accumulative_correct_count[index]) / Decimal(ld[index]))
            index = index + 1 
        detectionRate = Decimal(Decimal(detectionRate) / Decimal(len(label_disctribution)))
        accumulativeDetectionRate = Decimal(Decimal(accumulativeDetectionRate) / Decimal(len(label_disctribution)))
        self.team_detection_rate = detectionRate 
        self.accumulative_detection_rate = accumulativeDetectionRate 


    def updateActiveSymbionts(self):
        self.symbionts.sort(key = lambda i: i.getBid(), reverse=True)
        if len(self.active_symbionts) == 0 or self.symbionts[0] not in self.active_symbionts:
             self.active_symbionts.append(self.symbionts[0])
        self.active_symbionts = flatten(self.active_symbionts)     

    def is_similar(self, other):
        is_similar = False
        if isinstance(other, self.__class__):
            if self.action == other.action:
                is_similar = True;      
        return is_similar  

    def calculateScore(self):
        self.score = Decimal(Decimal(Decimal(1 - RELATIVE_NOVELTY_WEIGHT) * self.team_detection_rate) + Decimal(Decimal(RELATIVE_NOVELTY_WEIGHT) * self.distance))   

    def resetTeam(self):
        self.team_detection_rate = 0
        self.accumulative_detection_rate = 0
        self.team_error_rate = 0
        self.accumulative_error_rate = 0
        self.correct_count = []
        self.accumulative_correct_count = []
        index = 0
        while index < LABEL_COUNT:
            self.correct_count.append(0)
            self.accumulative_correct_count.append(0)
            index = index + 1

        
    def __init__(self, symbionts):
        self.symbionts = []
        self.symbionts = symbionts[:]
        self.active_symbionts = []
        self.action = -1
        self.distance = 0
        self.score = 0
        self.resetTeam()
        

    def __eq__(self, other):
        is_equal = False
        if isinstance(other, self.__class__):
            if self.score == other.score and self.team_detection_rate == other.team_detection_rate and self.distance == other.distance:
                is_equal = True;
                for ss in self.symbionts:
                    exists = False
                    for os in other.symbionts:
                        if ss == os:
                            exists = True
                            break
                    if not exists:
                        is_equal = False
                        break;        
        return is_equal        

    def __ne__(self, other):
        return not self.__eq__(other)  

    def __cmp__(self,other):
        return cmp(self.score,other.score)    

    def getSymbionts(self):
        return self.symbionts

    def setSymbionts(self, symbionts):
        self.symbionts.append(symbionts)

    def getActiveSymbionts(self):
        return self.active_symbionts

    def setActiveSymbionts(self, active_symbionts):
        self.active_symbionts.append(active_symbionts)    

    def getTeamDetectionRate(self):
        return self.team_detection_rate

    def getTeamErrorRate(self):
        return 1 - self.team_detection_rate   

    def setTeamDetectionRate(self, team_detection_rate):
        self.team_detection_rate = team_detection_rate 

    def getAccumulativeDetectionRate(self):
        return self.accumulative_detection_rate

    def getAccumulativeErrorRate(self):
        return 1 - self.accumulative_detection_rate    

    def setAccumulativeDetectionRate(self, accumulative_detection_rate):
        self.accumulative_detection_rate = accumulative_detection_rate     

    def getDistance(self):
        return self.distance

    def setDistance(self, distance):
        self.distance = distance          

    def getAction(self):
        return self.action   

    def getCorrectCount(self, label):
        return self.correct_count[label] 

    def getAccumulativeCorrectCount(self, label):
        return self.accumulative_correct_count[label] 
        
    def setAccumulativeCorrectCount(self, label, accumulative_correct_count):
        self.accumulative_correct_count[label] = accumulative_correct_count

    def getScore(self): 
        return self.score
