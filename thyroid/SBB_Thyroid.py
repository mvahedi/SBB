#!/usr/local/bin/python
__author__ = 'Maryam Vahedi'
import csv
import random
import math
import os
from collections import defaultdict
from decimal import *

###############################################################
###CONSTANTS - AKA CONFIGURATION
###############################################################

### initialization config
LABELS = ['1','2','3']
LABEL_COUNT = len(LABELS)
DATA_DELIMITER = ' '
OPERATORS = ['+', '-', '*', '/', 'cos', 'ln', 'exp', 'if']
OP_COUNT = len(OPERATORS)
LABEL_INDEX = 21

INSTRUCTION_POP_SIZE        = 50 
SYMBIONT_POP_SIZE           = 200
PROGRAM_MIN_INSTRUCTIONS    = 2
PROGRAM_MAX_INSTRUCTIONS    = 5
TRAINING_PERCENT            = 70
RELATIVE_NOVELTY_WEIGHT     = 0.5

TEAM_COUNT                  = 50
MONOLITHIC                  = False
MIN_TEAM_SIZE               = 2
MAX_TEAM_SIZE               = 10
POPULATION_REMOVAL_RATE     = 0.20
POPULATION_PARENT_RATE      = POPULATION_REMOVAL_RATE

### Rates for Variation Operators
TEAM_ADD_RATE               = 0.7
TEAM_DELETE_RATE            = 0.7
SYMBIONT_MODIFICATION_RATE  = 0.2
SYMBIONT_ACTION_CHANGE_RATE = 0.1
ADD_INSTRUCTION_RATE        = 0.5
DELETE_INSTRUCTION_RATE     = 0.5
INSTRUCTION_MUTATION_RATE   = 0.1
INSTRUCTION_SWAP_RATE       = 0.1
LABEL_SAMPLE_COUNT          = 50

### Number of times to try before we give up
MAX_ALLOWABLE_GENERATIONS   = 250
MIN_TEAM_SCORE = 0.85
SAVE_GENERATIONS = 5

### genotypic configurations
TARGET_COUNT = 4
SOURCE_COUNT = 21
MODE_BIT_COUNT = 1
OP_BIT_COUNT = 3
TARGET_BIT_COUNT = 2
SOURCE_BIT_COUNT = 5
ENCODED_BIT_COUNT = MODE_BIT_COUNT + OP_BIT_COUNT + TARGET_BIT_COUNT + SOURCE_BIT_COUNT
ENCODED_DECIMAL_EQUIVELANT = 2 ** ENCODED_BIT_COUNT


###############################################################
###Global Variables
###############################################################

generation = 0
data = []
data_count = 0
train_data = []
train_data_count = 0
test_data = []
test_data_count = 0
# Symbionts (Programs)
symbiont_population = []
# Instructions in programs
instruction_population = []
# Hosts (teams)
host_population = []
parent_host_population = []
offsprings = []
new_teams = []
label_disctribution = []
train_label_disctribution = []
test_label_disctribution = []
attributes_relevant_to_label = []

###############################################################
###CLASSES
###############################################################

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
        #print args
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
        if self.getTarget()  > TARGET_COUNT - 1:
            print "WHY?!?! ", self.getTarget(), " args: ", args   
            self.print_instruction()     
        args[0][self.getTarget()] = target
        return args[0]                        

    def print_instruction(self):
        if self.getTarget() > TARGET_COUNT - 1:
            print "******STOP****** WHYYYYYYYYYYYY "
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
                    print "WTF"
                    tvs = wtf.run_instruction(flatten(tvs), exemplar)
            else:
                tvs = s.run_instruction(flatten(tvs), exemplar)
            self.targetValues = flatten(tvs)          
        self.bid = self.getTargetValues()[0]       

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

    def getAttributes(self):
        sources = []
        for instruction in self.instructions:
            if instruction.getMode() == 0:
                s = instruction.getSource()
                if s not in sources:
                    sources.append(instruction.getSource())
        #print sources  
        sources = flatten(sources)
        sources.sort()        
        return sources        

class team:
    def evaluate_team(self, exemplar, updateAttributes = False):
        isCorrect = False
        for symbiont in self.symbionts:
            symbiont.reset()
            symbiont.evaluate(exemplar)    
        self.symbionts.sort(key = lambda i: i.getBid(), reverse=True)
        self.action = self.symbionts[0].getAction()
        if LABELS[self.action] == exemplar[LABEL_INDEX]:
            self.updateActiveSymbionts()
            isCorrect = True
            if updateAttributes == True:
                updateRelevantAttributesForLabels(self.action, self.symbionts[0].getAttributes())
            self.correct_count[self.action] = self.correct_count[self.action] + 1    
        return isCorrect

    def calculateDetectionRates(self, isTest = False, isAll=False):
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


#Functions

###############################################################
###UTILS
###############################################################

def flatten(l):
    flatList = []
    for elem in l:
        # if an element of a list is a list
        # iterate over this list and add elements to flatList 
        if type(elem) == list:
            for e in elem:
                flatList.append(e)
        else:
            flatList.append(elem)
    return flatList

###############################################################
###READ DATA
###############################################################
def read_data():
    read_data_file()
    sample_data()
    read_test_data()

def read_data_file(): 
    global data
    global data_count
    global label_disctribution
    print '****** Reading Data ... '
    with open('ann-train.data') as data_file:
        for line in data_file:
            data.append(line.strip().split(DATA_DELIMITER))

    data_count = len(data)
    index = 0
    while index < LABEL_COUNT:
        label_disctribution.append(0)
        index = index + 1
    for exemplar in data:
        i = 0
        for label in LABELS:
            if exemplar[LABEL_INDEX] == label:
                label_disctribution[i] = label_disctribution[i] + 1
            i = i + 1    

    i = 0 
    for label in LABELS:
        print "All # of rows in class: ", label, " is ", label_disctribution[i]
        i = i + 1
    print '****** Reading DONE!'          

def sample_data(): 
    global data_count
    global data
    global train_data
    global train_data_count
    global label_disctribution
    global train_label_disctribution
    train_data = []
    train_label_disctribution = []
    print '****** Sampling Data ... '
    random.shuffle(data)
    index = 0
    while index < LABEL_COUNT:
        train_label_disctribution.append(0)
        index = index + 1
    for exemplar in data:
        i = 0
        for label in LABELS:
            if exemplar[LABEL_INDEX] == label:
                if train_label_disctribution[i] < LABEL_SAMPLE_COUNT:
                    train_data.append(exemplar)
                    train_label_disctribution[i] = train_label_disctribution[i] + 1
            i = i + 1    

    i = 0 
    for label in LABELS:
        while train_label_disctribution[i] < LABEL_SAMPLE_COUNT:
            random.shuffle(data)
            for exemplar in data:
                if exemplar[LABEL_INDEX] == label:
                    if train_label_disctribution[i] < LABEL_SAMPLE_COUNT:
                        train_data.append(exemplar)
                        train_label_disctribution[i] = train_label_disctribution[i] + 1
        print "Sampling ", train_label_disctribution[i] ," rows in class: ", label, " out of ", label_disctribution[i]
        i = i + 1

    train_data_count = len(train_data)    
    print "Train Data Count ", train_data_count
    print '****** Sampling DONE!' 

def read_test_data(): 
    global test_data_count
    global test_data
    global test_label_disctribution
    with open('ann-test.data') as data_file:
        for line in data_file:
            test_data.append(line.strip().split(DATA_DELIMITER))
    
    test_data_count = len(test_data)
    print "Test Data Count ", test_data_count
    index = 0
    while index < LABEL_COUNT:
        test_label_disctribution.append(0)
        index = index + 1
    for exemplar in test_data:
        i = 0
        for label in LABELS:
            if exemplar[LABEL_INDEX] == label:
                test_label_disctribution[i] = test_label_disctribution[i] + 1
            i = i + 1    
    i = 0 
    for label in LABELS:
        print "ALL # of rows in class for test data: ", label, " is ", test_label_disctribution[i]
        i = i + 1  

def read_train_data(): 
    global train_data_count
    global train_data
    global train_label_disctribution
    train_label_disctribution = []
    train_data = []
    with open('ann-train.data') as data_file:
        for line in data_file:
            train_data.append(line.strip().split(DATA_DELIMITER))
    train_data_count = len(train_data)
    print "All training Data Count ", train_data
    index = 0
    while index < LABEL_COUNT:
        train_label_disctribution.append(0)
        index = index + 1
    for exemplar in train_data:
        i = 0
        for label in LABELS:
            if exemplar[LABEL_INDEX] == label:
                train_label_disctribution[i] = train_label_disctribution[i] + 1
            i = i + 1    
    i = 0 
    for label in LABELS:
        print "ALL # of rows in class for training data: ", label, " is ", train_label_disctribution[i]
        i = i + 1         

###############################################################
###INITIALIZE
###############################################################

#This function randomly generates an instruction gene and returns the instruction
#NOTE: for some reason it doesn't work! The instruction works fine
#I don't understand why!!!!
def generate_instructions_from_code():
    greys = gcgen(ENCODED_BIT_COUNT)
    instructions_in_population = random.randint(0, ENCODED_DECIMAL_EQUIVELANT)
    encoded_string = str(greys[instructions_in_population])
    s = decode(encoded_string)
    s.print_instruction()
    return s 

#This function generates and returns an instruction 
#used for initiating the environment
def generate_instructions():
    mode = random.randint(0, 1)
    target = random.randint(0, TARGET_COUNT - 1)
    opcode = random.randint(0, OP_COUNT - 1)
    source = random.randint(0, SOURCE_COUNT - 1)
    i = instruction(mode, target, opcode, source, str(encode(mode,target,opcode,source)))
    i.print_instruction()
    return i
    
#This function initiates the instruction population    
def initiate_instructions():
    global instruction_population
    p = 0
    while p < INSTRUCTION_POP_SIZE:
        new_instruction = generate_instructions()
        if new_instruction not in instruction_population:
            instruction_population.append(new_instruction)  
            p = p + 1        

def initiate_symbiont_population():
    global instruction_population
    initiate_instructions()
    symbionts = []
    p = 0
    while p < SYMBIONT_POP_SIZE:
        instruction = []
        number_of_instructions_in_program = random.randint(PROGRAM_MIN_INSTRUCTIONS, PROGRAM_MAX_INSTRUCTIONS)
        program_instructions = random.sample(range(0, INSTRUCTION_POP_SIZE-1), number_of_instructions_in_program)
        #program_instructions = random.sample(range(0, INSTRUCTION_POP_SIZE-1), PROGRAM_MAX_INSTRUCTIONS)
        i = 0
        for program_instruction in program_instructions:
            instruction.append(instruction_population[program_instructions[i]])
            i = i + 1
        symbiont_action = random.randint(0, LABEL_COUNT-1)
        ind =  symbiont(instruction, symbiont_action)
        symbionts.append(ind)
        p = p + 1
        print "Symbiont:  ", p, " Action: ", symbiont_action , " # of instructions: ", number_of_instructions_in_program, " instruction Length: ", len(instruction)
    return symbionts

def initiate_teams():
    global symbiont_population
    global host_population
    symbiont_population = initiate_symbiont_population()
    i = 0
    while i < TEAM_COUNT:
        symbionts = []
        symbiont_count_in_team = random.randint(MIN_TEAM_SIZE, MAX_TEAM_SIZE)
        team_symbionts = random.sample(range(0, INSTRUCTION_POP_SIZE-1), symbiont_count_in_team)
        p = 0
        for symbiont in team_symbionts:
            symbionts.append(symbiont_population[team_symbionts[p]])
            p = p + 1       
        multyActionTeam(symbionts)
        t =  team(symbionts)
        host_population.append(t)
        i = i + 1
    clean_symbionts() 

def multyActionTeam(symbionts):
    global symbiont_population
    action = None
    previous_action = None
    more_than_one_action = False    
    for s in symbionts:
        action = s.getAction()
        if previous_action != action:
            more_than_one_action = True
        else:
            previous_action = action

    while True:   
        symbiont_index = random.randint(0, len(symbiont_population)-1) 
        new_symbiont = symbiont_population[symbiont_index]
        new_symbiont_action = new_symbiont.getAction() 
        if new_symbiont_action != action:
            break

    index_to_replace = random.randint(0, len(symbionts)-1) 
    symbionts.insert(index_to_replace, new_symbiont)
    del symbionts[index_to_replace + 1]

###############################################################
###GENE OPERATORS
###############################################################

#MODE TARGET OPCODE SOURCE
#0 000 000 000
def encode(mode,target,opcode,source):
    target_greys = gcgen(TARGET_BIT_COUNT)
    op_greys = gcgen(OP_BIT_COUNT)
    source_greys = gcgen(SOURCE_BIT_COUNT)
    print target, " ", opcode, " ", source
    encoded_string = str(str(mode) + target_greys[target] + op_greys[opcode] + source_greys[source])
    return str(encoded_string)

def graycode(numbits, reverse = False):
    if numbits == 1:
        if reverse:
            yield "1"
            yield "0"
        else:
            yield "0"
            yield "1"
    else:
        if reverse:
            # all the "1"s start first
            gcprev = graycode(numbits - 1, True)
            for code in gcprev:
                yield "1" + code

            gcprev = graycode(numbits - 1, False)
            for code in gcprev:
                yield "0" + code
        else:
            # all the "0" start first
            gcprev = graycode(numbits - 1, False)
            for code in gcprev:
                yield "0" + code

            gcprev = graycode(numbits - 1, True)
            for code in gcprev:
                yield "1" + code

def gcgen(numbits = 2, reverse = False):
    i = 0
    greys = []
    for codes in graycode(numbits, reverse):
        greys.append(codes)
    return greys    

def decode(encoded):
    target_greys = gcgen(TARGET_BIT_COUNT)
    op_greys = gcgen(OP_BIT_COUNT)
    source_greys = gcgen(SOURCE_BIT_COUNT);
    #print 'decoding: ', encoded
    if len(encoded) < OP_BIT_COUNT + TARGET_BIT_COUNT + SOURCE_BIT_COUNT:
        mode = 0
        target = target_greys.index(str(encoded[0:TARGET_BIT_COUNT]))
        opcode = op_greys.index(str(encoded[TARGET_BIT_COUNT:TARGET_BIT_COUNT+OP_BIT_COUNT]))
        source = source_greys.index(str(encoded[TARGET_BIT_COUNT+OP_BIT_COUNT:]))
    else:
        mode = encoded[0]
        target = target_greys.index(str(encoded[1:TARGET_BIT_COUNT+1]))
        opcode = op_greys.index(str(encoded[TARGET_BIT_COUNT+1:TARGET_BIT_COUNT+OP_BIT_COUNT+1]))
        source = source_greys.index(str(encoded[TARGET_BIT_COUNT+OP_BIT_COUNT+1:]))
    return instruction(mode, target, opcode, source, encoded)

###############################################################
###VARIATION OPERATORS
###############################################################

# Instruction Variation Operator Mutate
def mutate(encoded):
    char_size = len(encoded)
    bitToMutate = random.randint(0, char_size - 1)
    #print ('before mutation ' , encoded , ' mutating bit # ' , bitToMutate)
    if encoded[bitToMutate] == '0':
        b_s = bytearray(encoded)
        b_s[bitToMutate] = '1'
        encoded = str(b_s)
    else:
        b_s = bytearray(encoded)
        b_s[bitToMutate] = '0'
        encoded = str(b_s)
    #print ('after mutation ' , encoded)    
    return encoded    

# Instruction Variation Operator Crossover
def crossover(parent1, parent2):
    offsprings = []
    crossover_point = random.randint(1, 9)
    parent1_decoded = parent1.getEncoded()
    parent2_decoded = parent2.getEncoded()
    offspring1_decoded = parent1_decoded[:crossover_point] + parent2_decoded[crossover_point:]
    offspring2_decoded = parent2_decoded[:crossover_point] + parent1_decoded[crossover_point:]
    offspring1 = decode(offspring1_decoded)
    offspring2 = decode(offspring2_decoded)
    offsprings.append(offspring1)
    offsprings.append(offspring2)
    #print '# of offspring after crossover ', len(offsprings)
    return offsprings

# 1- Randomly select an instruction from the global instruction_population
# 2- Randomly select an instruction from the indovidual
# 3- Replace the randomply selected instruction in step 2 with the instruction selected in step 1
def add_instruction(selected_symbiont):
    global instruction_population
    symbiont_instructions = []
    new_symbiont = None
    symbiont_instructions = flatten(selected_symbiont.getInstructions())
    if len(symbiont_instructions) < PROGRAM_MAX_INSTRUCTIONS:
        instruction_population = flatten(instruction_population)
        new_instruction_index = random.randint(0, len(instruction_population)-1)
        index = random.randint(0, len(symbiont_instructions)-1)
        symbiont_instructions.insert(index, instruction_population[new_instruction_index])
        new_symbiont = symbiont(symbiont_instructions, selected_symbiont.getAction())
    return new_symbiont

def remove_instruction(selected_symbiont):
    symbiont_instructions = []
    symbiont_instructions = flatten(selected_symbiont.getInstructions())
    if len(symbiont_instructions) > PROGRAM_MIN_INSTRUCTIONS:
        index = random.randint(0, len(symbiont_instructions)-1)
        del symbiont_instructions[index]
        new_symbiont = symbiont(symbiont_instructions, selected_symbiont.getAction())
        return new_symbiont
    return None       

# 1- Randomly select an instruction from the symbionts instructions
# 2- Mutate randomly selected instruction to create a new instruction
# 3- Add the new (mutated) instruction to the global instruction_population
# 4- Replace the new instruction in the symbiont with the old one
# Note: The old instruction will remain in the instruction population until the next generation of instructions are selected
def create_new_program_by_mutation(selected_symbiont):
    global instruction_population
    symbiont_instructions = []
    symbiont_instructions = flatten(selected_symbiont.getInstructions())
    #print symbiont_instructions
    index = random.randint(0, len(symbiont_instructions)-1)
    #print "index", index
    if type(symbiont_instructions[index]) is list:
        for ind in symbiont_instructions[index]:
            ind.print_instruction()
    mutated_instruction = decode(mutate(symbiont_instructions[index].getEncoded()))
    if mutated_instruction not in instruction_population:
        instruction_population.append(mutated_instruction)

    del symbiont_instructions[index]
    symbiont_instructions.insert(index, mutated_instruction)
    new_symbiont = symbiont(symbiont_instructions, selected_symbiont.getAction())
    return new_symbiont  

def create_new_program_by_instruction_swap(selected_symbiont):
    new_symbiont = selected_symbiont
    symbiont_instructions = []
    symbiont_instructions = flatten(selected_symbiont.getInstructions())
    if len(symbiont_instructions) > 1:
        print "# of Instruction: ", len(symbiont_instructions)
        instructions_to_swap = random.sample(range(0, len(symbiont_instructions)), 2)
        instructions = new_symbiont.getInstructions()
        instructions[instructions_to_swap[0]], instructions[instructions_to_swap[1]] = instructions[instructions_to_swap[1]], instructions[instructions_to_swap[0]]
        new_symbiont.setInstructions(instructions)
    return new_symbiont                 

def apply_variation_operators_to_symbionts(parent_population):
    new_symbiont = []
    for i in parent_population:
        temp_symbiont = i
        new_temp_symbionts = []
        if random.random() < ADD_INSTRUCTION_RATE:
            added = add_instruction(temp_symbiont)
            if added != None:
                temp_symbiont = added
        if random.random() < DELETE_INSTRUCTION_RATE:
            temp = remove_instruction(temp_symbiont) 
            if temp is not None:
                temp_symbiont = temp
        if random.random() < INSTRUCTION_MUTATION_RATE:
            temp_symbiont = create_new_program_by_mutation(temp_symbiont)
        if random.random() < INSTRUCTION_SWAP_RATE:
            temp_symbiont = create_new_program_by_instruction_swap(temp_symbiont)
        if random.random() < SYMBIONT_ACTION_CHANGE_RATE:
            new_symbiont_action = random.randint(0, LABEL_COUNT-1)
            while new_symbiont_action == temp_symbiont.getAction():
                new_symbiont_action = random.randint(0, LABEL_COUNT-1)
            temp_symbiont.setAction(new_symbiont_action)       
        new_symbiont.append(temp_symbiont)
    return new_symbiont           
    
def evolve_teams():
    global parent_host_population
    global new_teams
    global generation
    global symbiont_population
    del new_teams[:] 
    print 'EVOLVING', len(parent_host_population), 'TEAMS IN GENERATION ', generation 
    i = 1
    for host in flatten(parent_host_population):
        changed = False
        team_symbionts = host.getSymbionts()
        new_team_symbionts = team_symbionts[:]

        if random.random() < TEAM_DELETE_RATE:
            #REMOVE
            if len(new_team_symbionts) > MIN_TEAM_SIZE:
                print 'Team ', i, ' Deleting symbiont'
                symbiont_to_delete = random.randint(0, len(new_team_symbionts)-1)
                del new_team_symbionts[symbiont_to_delete]
                changed = True

        if random.random() < TEAM_ADD_RATE:
            #ADD
            if len(new_team_symbionts) > MIN_TEAM_SIZE and len(new_team_symbionts) < MAX_TEAM_SIZE:
                print 'Team ', i, ' Adding new symbionts'
                new_symbiont_index = random.randint(0, len(symbiont_population)-1)    
                new_team_symbionts.append(symbiont_population[new_symbiont_index])
                changed = True 

        if random.random() < SYMBIONT_MODIFICATION_RATE:        
            #Apply Variation to team symbionts
            new_team_symbionts = apply_variation_operators_to_symbionts(new_team_symbionts)
            changed = True

        if changed == True:
            multyActionTeam(new_team_symbionts)    
            print 'adding new team!!!'
            new_teams.append(team(new_team_symbionts)) 
        i = i + 1       
        new_teams =  flatten(new_teams)
    print '# of new teams in generation: ', generation, ' is: ', len(new_teams)

###############################################################
###SELECTION
###############################################################
def printTeams():
    global host_population
    j = 0
    for host in host_population: 
        print 'Team: ', j, 'Team Action: ' ,host.getAction(), ' Detection Rate: ', host.getTeamDetectionRate(), ' Accumulative Detection Rate: ', host.getAccumulativeDetectionRate(), ' Distance: ', host.getDistance() , ' # of active symbionts: ', len(host.getActiveSymbionts()), ' SCORE: ', host.getScore()
        j = j + 1

def saveGenerationResults(isTest = False, isAll = False):
    global host_population
    global generation
    generation_results = []
    host_population.sort(key = lambda i: i.getTeamDetectionRate(), reverse=True)
    for i in range(len(host_population)):        
        generation_results.append({"Host":i,"TeamAction":host_population[i].getAction(),
            "DetectionRate":host_population[i].getTeamDetectionRate(),
            "AccumulativeDetectionRate":host_population[i].getAccumulativeDetectionRate(),
            "ErrorRate":host_population[i].getTeamErrorRate(),
            "AccumulativeErrorRate":host_population[i].getAccumulativeErrorRate(),
            "Distance":host_population[i].getDistance(),
            "ActiveSymbiontCount":len(host_population[i].getActiveSymbionts()),"Score":host_population[i].getScore()})
    directory = os.path.join('results/')
    if not os.path.exists(os.path.dirname(directory)):
        try:
            os.makedirs(os.path.dirname(directory))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    if isTest == True:
        filename = directory + "thyroid_test_data.csv"
    elif isAll == True:
        filename = directory + "thyroid_all_data.csv"    
    else:               
        filename = directory + 'thyroid_genration' + str(generation) + '.csv'            
    try:
        fp = open(filename)
    except IOError:
        # If not exists, create the file
        fp = open(filename, 'wb')
        
    print "writing to file: ", filename
    headings = ['Host','TeamAction','DetectionRate', 'AccumulativeDetectionRate','ErrorRate', 'AccumulativeErrorRate',"Distance",'ActiveSymbiontCount','Score']   
    try:
        with fp as myfile:
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(headings)
            for row in generation_results:
                wr.writerow([row['Host'],row['TeamAction']
                    , row['DetectionRate'], row['AccumulativeDetectionRate']
                    , row['ErrorRate'], row['AccumulativeErrorRate']
                    , row["Distance"],row['ActiveSymbiontCount'],row['Score']])
    finally:
        myfile.close() 
    if isTest or isAll:               
        printAllRelevantAttributesForLabels(isTest, isAll)              

def checkGeneration():
    global host_population
    teams_are_good = False
    host_population = flatten(host_population)
    print len(host_population)
    if host_population[len(host_population)-1].getScore() >= MIN_TEAM_SCORE:
        teams_are_good = True
    return teams_are_good

def calculateTeamDistance(team1, team2):
    distance = 1
    intersect_count = 0
    union_count = 0
    team1_symbionts = team1.getActiveSymbionts()
    team2_symbionts = team2.getActiveSymbionts()
    for team1_symbiont in team1_symbionts:
        if team1_symbiont in team2_symbionts:
            intersect_count = intersect_count + 1
        else:
            union_count = union_count + 1    
    union_count = union_count + (len(team2_symbionts) - intersect_count)
    if union_count != 0:
        distance = Decimal((Decimal(distance) - Decimal((Decimal(intersect_count)/Decimal(union_count)))))
    return distance           

def resetRelevantAttributesForLables():
    global attributes_relevant_to_label
    index = 0
    while index < LABEL_COUNT:
        attributes = []
        attributes_relevant_to_label.append(attributes)
        index = index + 1

def updateRelevantAttributesForLabels(label, *attributes):
    global attributes_relevant_to_label
    empty = []
    for attribute in attributes:
        if attribute not in attributes_relevant_to_label[label]:
            attributes_relevant_to_label[label].append(attribute) 
    if empty in attributes_relevant_to_label[label]:
        attributes_relevant_to_label[label].remove(empty)            
    attributes_relevant_to_label[label].sort()               

def printAllRelevantAttributesForLabels(isTest, isAll):
    global attributes_relevant_to_label
    global generation
    directory = os.path.join('results/')
    if not os.path.exists(os.path.dirname(directory)):
        try:
            os.makedirs(os.path.dirname(directory))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    if isTest == True:
        filename = directory + "thyroid_test_attributes.csv"
    elif isAll == True:
        filename = directory + "thyroid_all_attributes.csv"    
    else:               
        filename = directory + 'thyroid_attributes' + str(generation) + '.csv'            
    try:
        fp = open(filename)
    except IOError:
        # If not exists, create the file
        fp = open(filename, 'wb')
        
    print "writing to file: ", filename
    try:
        with fp as f:
            writer = csv.writer(f)
            writer.writerows(attributes_relevant_to_label)
    finally:
        f.close()        
    index = 0
    while index < LABEL_COUNT:
        print "Label: ", index, " Attributes: ", attributes_relevant_to_label[index]
        index = index + 1

def rank_teams(isTest = False, isAll = False):
    global host_population
    global data_count
    global train_data_count
    global test_data_count
    global test_data
    global train_data
    global data
    if isTest:
        print '****** Ranking Teams with Test data - DATA COUNT: ', test_data_count
        rankData = test_data
    elif isAll:
        print '****** Ranking Teams with ALL data - DATA COUNT: ', data_count
        rankData = data  
    else:
        print '****** Ranking Teams with Training data - DATA COUNT: ', train_data_count 
        rankData = train_data 

    host_population = flatten(host_population)

    for host in host_population:
        host.resetTeam()

    for exemplar in rankData:
        for host in host_population:
            host.evaluate_team(exemplar, isTest or isAll)

    for host in host_population:
        host.calculateDetectionRates(isTest, isAll)

    host_population.sort(key = lambda i: i.getTeamDetectionRate(), reverse=True)

    for host in host_population:
        host.resetTeam()

    for exemplar in rankData:
        isDetected = False;
        label = LABELS.index(exemplar[LABEL_INDEX])
        for host in host_population:
            isCorrect = host.evaluate_team(exemplar, isTest or isAll)
            if isCorrect or isDetected:
                acc = host.getAccumulativeCorrectCount(label) + 1
                host.setAccumulativeCorrectCount(label, acc)
                isDetected = True              

    host_id = 1            
    for host in host_population:
        host_id = host_id + 1
        host.calculateDetectionRates(isTest, isAll)          

    #Calculate team distances
    for host in host_population:
        host_average_distance = 0
        for other_host in host_population: 
            host_average_distance = host_average_distance + calculateTeamDistance(host, other_host)
        host_average_distance = Decimal(host_average_distance / len(host_population))
        host.setDistance(host_average_distance)  
        host.calculateScore()     


def evaluate_teams():
    global generation
    global host_population
    global parent_host_population
    global new_teams
    optimal_detection_rate_reached = False
    print "****** Evaluating ", len(host_population), " teams ******"
    host_population.extend(new_teams)
    del parent_host_population[:]
    remove_similar_teams()
    #printTeams()
    rank_teams()
    host_population = flatten(host_population)
    host_population = [i for i in host_population if i is not None]
    host_population.sort(key = lambda i: i.getScore(), reverse=True)
    printTeams()  
    return checkGeneration()

def cleanup():
    if len(host_population) > TEAM_COUNT:
        #Remove the bad teams botom 20%
        delete_count = len(host_population) - TEAM_COUNT
        delete_count = delete_count + int(len(host_population) * POPULATION_REMOVAL_RATE)
        del host_population[-delete_count:]
        print "AFTER REMOVING ", delete_count, " TEAMS: ", len(host_population)
    clean_symbionts()


def selectParents():
    global host_population
    global parent_host_population
    #Select parent teams
    del parent_host_population[:]
    parent_count = int(len(host_population) * POPULATION_PARENT_RATE)
    parent_indexes = random.sample(range(0, len(host_population)-1), parent_count)
    for i in parent_indexes:
        parent_host_population.append(host_population[i])
    parent_host_population = flatten(parent_host_population)
    print "****** Parent population: ", len(parent_host_population)
    j = 0
    for host in parent_host_population: 
        print 'Team: ', j, 'Team Action: ' ,host.getAction(), ' Team Score: ', host.getScore()
        j = j + 1  

def remove_similar_teams():
    global generation
    global host_population
    new_host_population = []
    print '****** removing similar teams in generation: ', generation
    print 'number of teams: ', len(host_population)
    i = 0
    for first_team in host_population:
        j = i + 1
        is_duplicate = False
        while j < len(host_population):
            if host_population[i] == host_population[j]:
                is_duplicate = True
                break
            j = j + 1
        if not is_duplicate:
            new_host_population.append(first_team)
        i= i + 1
    host_population =  new_host_population[:] 
    print 'number of unique teams: ', len(host_population)      


def clean_symbionts():
    global symbiont_population
    global host_population
    host_population = flatten(host_population)
    host_population = [i for i in host_population if i is not None]
    del symbiont_population[:]
    for i in host_population:
        team_symbionts = i.getSymbionts()
        for s in team_symbionts:
            if s not in symbiont_population:
                symbiont_population.append(s) 
    clean_instruction_population()   

def clean_instruction_population():
    global instruction_population
    global symbiont_population
    symbiont_population = flatten(symbiont_population)
    symbiont_population = [i for i in symbiont_population if i is not None]
    del instruction_population[:]
    for i in symbiont_population:
        program_instructions = i.getInstructions()
        for s in program_instructions:
            if s not in instruction_population:
                instruction_population.append(s)         

def run_gp():
    global generation
    global symbiont_population
    global host_population
    print '****** Initial host population size: ', len(host_population)
    stop_criteria_met = False
    while (stop_criteria_met == False):
        resetRelevantAttributesForLables()
        generation+=1
        optimal_detection_rate_reached = evaluate_teams()
        # Only save results for every 10 generation
        if generation == 1 or generation % SAVE_GENERATIONS == 0 or optimal_detection_rate_reached:
            saveGenerationResults()
        # Last generation    
        if generation == MAX_ALLOWABLE_GENERATIONS or optimal_detection_rate_reached:
            stop_criteria_met = True
            print "****** FINAL TEAMS: "
            #All Data
            rank_teams(False, True)
            saveGenerationResults(False, True)

            #Test Data
            rank_teams(True)
            saveGenerationResults(True)
        else: 
            cleanup()  
            sample_data() 
            selectParents()
            evolve_teams()   
    print 'Total number of generations: ', generation

###############################################################
###START
###############################################################

read_data()
initiate_teams()
run_gp()

###############################################################
###END
###############################################################