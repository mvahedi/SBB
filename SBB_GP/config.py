# Fall-Winter 2016 
__author__ = 'Maryam Vahedi'
###############################################################
###CONSTANTS - AKA CONFIGURATION
###############################################################
import csv
import random
import math
import os
from collections import defaultdict
from decimal import *

### initialization config
### default values are for Iris
LABELS = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
def getLABELS():
	global LABELS
	return LABELS
def setLABELS(new_LABELS):
	global LABELS
	LABELS = new_LABELS

LABEL_COUNT = len(getLABELS())
def getLABEL_COUNT():
	global LABEL_COUNT
	return LABEL_COUNT

DATA_DELIMITER = ','
def getDATA_DELIMITER():
	global DATA_DELIMITER
	return DATA_DELIMITER
def setDATA_DELIMITER(new_DATA_DELIMITER):
	global DATA_DELIMITER
	DATA_DELIMITER = new_DATA_DELIMITER

OPERATORS = ['+', '-', '*', '/', 'cos', 'ln', 'exp', 'if']
def getOPERATORS():
	global OPERATORS
	return OPERATORS
def setOPERATORS(new_OPERATORS):
	global OPERATORS
	OPERATORS = new_OPERATORS

OP_COUNT = len(getOPERATORS())
def getOP_COUNT():
	global OP_COUNT
	return OP_COUNT

LABEL_INDEX = 4
def getLABEL_INDEX():
	global LABEL_INDEX
	return LABEL_INDEX
def setLABEL_INDEX(new_LABEL_INDEX):
	global LABEL_INDEX
	LABEL_INDEX = new_LABEL_INDEX


INSTRUCTION_POP_SIZE        = 100 
def getINSTRUCTION_POP_SIZE():
	global INSTRUCTION_POP_SIZE
	return INSTRUCTION_POP_SIZE

SYMBIONT_POP_SIZE           = 500
def getSYMBIONT_POP_SIZE():
	global SYMBIONT_POP_SIZE
	return SYMBIONT_POP_SIZE

PROGRAM_MIN_INSTRUCTIONS    = 2
def getPROGRAM_MIN_INSTRUCTIONS():
	global PROGRAM_MIN_INSTRUCTIONS
	return PROGRAM_MIN_INSTRUCTIONS

PROGRAM_MAX_INSTRUCTIONS    = 48
def getPROGRAM_MAX_INSTRUCTIONS():
	global PROGRAM_MAX_INSTRUCTIONS
	return PROGRAM_MAX_INSTRUCTIONS

TRAINING_PERCENT            = 70
def getTRAINING_PERCENT():
	global TRAINING_PERCENT
	return TRAINING_PERCENT

RELATIVE_NOVELTY_WEIGHT     = 0.5
def getRELATIVE_NOVELTY_WEIGHT():
	global RELATIVE_NOVELTY_WEIGHT
	return RELATIVE_NOVELTY_WEIGHT

TEAM_COUNT                  = 50
def getTEAM_COUNT():
	global TEAM_COUNT
	return TEAM_COUNT

MONOLITHIC                  = False
def getMONOLITHIC():
	global MONOLITHIC
	return MONOLITHIC

MIN_TEAM_SIZE               = 2
def getMIN_TEAM_SIZE():
	global MIN_TEAM_SIZE
	return MIN_TEAM_SIZE

MAX_TEAM_SIZE               = 10
def getMAX_TEAM_SIZE():
	global MAX_TEAM_SIZE
	return MAX_TEAM_SIZE

POPULATION_REMOVAL_RATE     = 0.20
def getPOPULATION_REMOVAL_RATE():
	global POPULATION_REMOVAL_RATE
	return POPULATION_REMOVAL_RATE

POPULATION_PARENT_RATE      = POPULATION_REMOVAL_RATE
def getPOPULATION_PARENT_RATE():
	global POPULATION_PARENT_RATE
	return POPULATION_PARENT_RATE

### Rates for Variation Operators
TEAM_ADD_RATE               = 0.7
def getTEAM_ADD_RATE():
	global TEAM_ADD_RATE
	return TEAM_ADD_RATE

TEAM_DELETE_RATE            = 0.7
def getTEAM_DELETE_RATE():
	global TEAM_DELETE_RATE
	return TEAM_DELETE_RATE

SYMBIONT_MODIFICATION_RATE  = 0.2
def getSYMBIONT_MODIFICATION_RATE():
	global SYMBIONT_MODIFICATION_RATE
	return SYMBIONT_MODIFICATION_RATE

SYMBIONT_ACTION_CHANGE_RATE = 0.1
def getSYMBIONT_ACTION_CHANGE_RATE():
	global SYMBIONT_ACTION_CHANGE_RATE
	return SYMBIONT_ACTION_CHANGE_RATE

ADD_INSTRUCTION_RATE        = 0.5
def getADD_INSTRUCTION_RATE():
	global ADD_INSTRUCTION_RATE
	return ADD_INSTRUCTION_RATE

DELETE_INSTRUCTION_RATE     = 0.5
def getDELETE_INSTRUCTION_RATE():
	global DELETE_INSTRUCTION_RATE
	return DELETE_INSTRUCTION_RATE

INSTRUCTION_MUTATION_RATE   = 0.1
def getINSTRUCTION_MUTATION_RATE():
	global INSTRUCTION_MUTATION_RATE
	return INSTRUCTION_MUTATION_RATE

INSTRUCTION_SWAP_RATE       = 0.1
def getINSTRUCTION_SWAP_RATE():
	global INSTRUCTION_SWAP_RATE
	return INSTRUCTION_SWAP_RATE


### Number of times to try before we give up
MAX_ALLOWABLE_GENERATIONS   = 50
def getMAX_ALLOWABLE_GENERATIONS():
	global MAX_ALLOWABLE_GENERATIONS
	return MAX_ALLOWABLE_GENERATIONS

MIN_TEAM_SCORE = 0.85
def getMIN_TEAM_SCORE():
	global MIN_TEAM_SCORE
	return MIN_TEAM_SCORE

### genotypic configurations
TARGET_COUNT = 2
def getTARGET_COUNT():
	global TARGET_COUNT
	return TARGET_COUNT
def setTARGET_COUNT(new_TARGET_COUNT):
	global TARGET_COUNT
	TARGET_COUNT = new_TARGET_COUNT

SOURCE_COUNT = 4
def getSOURCE_COUNT():
	global SOURCE_COUNT
	return SOURCE_COUNT
def setSOURCE_COUNT(new_SOURCE_COUNT):
	global SOURCE_COUNT
	SOURCE_COUNT = new_SOURCE_COUNT

MODE_BIT_COUNT = 1
def getMODE_BIT_COUNT():
	global MODE_BIT_COUNT
	return MODE_BIT_COUNT

OP_BIT_COUNT = 3
def getOP_BIT_COUNT():
	global OP_BIT_COUNT
	return OP_BIT_COUNT

TARGET_BIT_COUNT = 1
def getTARGET_BIT_COUNT():
	global TARGET_BIT_COUNT
	return TARGET_BIT_COUNT
def setTARGET_BIT_COUNT(new_TARGET_BIT_COUNT):
	global TARGET_BIT_COUNT
	TARGET_BIT_COUNT = new_TARGET_BIT_COUNT

SOURCE_BIT_COUNT = 2
def getSOURCE_BIT_COUNT():
	global SOURCE_BIT_COUNT
	return SOURCE_BIT_COUNT
def setSOURCE_BIT_COUNT(new_SOURCE_BIT_COUNT):
	global SOURCE_BIT_COUNT
	SOURCE_BIT_COUNT = new_SOURCE_BIT_COUNT

ENCODED_BIT_COUNT = MODE_BIT_COUNT + OP_BIT_COUNT + TARGET_BIT_COUNT + SOURCE_BIT_COUNT
def getENCODED_BIT_COUNT():
	global ENCODED_BIT_COUNT
	return ENCODED_BIT_COUNT

ENCODED_DECIMAL_EQUIVELANT = 2 ** ENCODED_BIT_COUNT
def getENCODED_DECIMAL_EQUIVELANT():
	global ENCODED_DECIMAL_EQUIVELANT
	return ENCODED_DECIMAL_EQUIVELANT

SAVE_GENERATIONS = 5
def getSAVE_GENERATIONS():
	global SAVE_GENERATIONS
	return SAVE_GENERATIONS


###############################################################
###Global Variables
###############################################################

generation = 0
def get_generation():
	global generation
	return generation
def set_generation(new_generation):
	global generation
	generation = new_generation

data = []
def get_data():
	global data
	return data
def get_random_data():
	global data
	random.shuffle(data) 
	return data	
def set_data(new_data):
	global data
	data = new_data
def append_data(new_data):
	global data
	data.append(new_data)	

data_count = 0
def get_data_count():
	global data
	return len(data)

train_data = []
def get_train_data():
	global train_data
	return train_data
def set_train_data(new_train_data):
	global train_data
	train_data = new_train_data
def append_train_data(new_train_data):
	global train_data
	train_data.append(new_train_data)	

train_data_count = 0
def get_train_data_count():
	global train_data
	return len(train_data)

test_data = []
def get_test_data():
	global test_data
	return test_data
def set_test_data(new_test_data):
	global test_data
	test_data = new_test_data
def append_test_data(new_test_data):
	global test_data
	test_data.append(new_test_data)	

test_data_count = 0
def get_test_data_count():
	global test_data
	return len(test_data)

# Symbionts (Programs)
symbiont_population = []
def get_symbiont_population():
	global symbiont_population
	return symbiont_population
def set_symbiont_population(new_symbiont_population):
	global symbiont_population
	symbiont_population = new_symbiont_population
def append_symbiont_population(new_symbiont_population):
	global symbiont_population
	symbiont_population.append(new_symbiont_population)	
def delete_symbiont_population():
	global symbiont_population
	del symbiont_population[:]
	


# Instructions in programs
instruction_population = []
def get_instruction_population():
	global instruction_population
	return instruction_population
def set_instruction_population(new_instruction_population):
	global instruction_population
	instruction_population = new_instruction_population	
def append_instruction_population(new_instruction):
	global instruction_population
	instruction_population.append(new_instruction)
def delete_instruction_population():
	global instruction_population
	del instruction_population[:]	

# Hosts (teams)
host_population = []
def get_host_population():
	global host_population
	return host_population
def set_host_population(new_host_population):
	global host_population
	host_population = new_host_population
def apend_host_population(new_host_population):
	global host_population
	host_population.append(new_host_population)
def sort_host_population():
	global host_population
	host_population.sort(key = lambda i: i.getTeamDetectionRate(), reverse=True)
def sort_by_score_host_population():
	global host_population
	host_population.sort(key = lambda i: i.getScore(), reverse=True)		
def extend_host_population(new_teams):
	global host_population
	host_population.extend(new_teams)
def get_host_population_length():
	global host_population
	return len(host_population)

parent_host_population = []
def get_parent_host_population():
	global parent_host_population
	return parent_host_population
def set_parent_host_population(new_parent_host_population):
	global parent_host_population
	parent_host_population = new_parent_host_population
def append_parent_host_population(new_parent_host_population):
	global parent_host_population
	parent_host_population.append(new_parent_host_population)
def delete_parent_host_population():
	global parent_host_population
	del parent_host_population[:]	

offsprings = []
def get_offsprings():
	global offsprings
	return offsprings
def set_offsprings(new_offsprings):
	global offsprings
	offsprings = new_offsprings

new_teams = []
def get_new_teams():
	global new_teams
	return new_teams
def set_new_teams(new_new_teams):
	global new_teams
	new_teams = new_new_teams
def append_new_teams(new_new_teams):
	global new_teams
	new_teams.append(new_new_teams)	
def delete_new_teams():
	del new_teams[:] 


label_distribution = []
def get_all_label_distribution():
	global label_distribution
	return label_distribution
def get_label_distribution(i):
	global label_distribution
	return label_distribution[i]	
def set_label_distribution(new_label_distribution):
	global label_distribution
	label_distribution = new_label_distribution
def append_label_distribution(new_label_distribution):
	global label_distribution
	label_distribution.append(new_label_distribution)	
def increment_label_distribution(i):
	global label_distribution
	label_distribution[i] = label_distribution[i] + 1	

train_label_distribution = []
def get_all_train_label_distribution():
	global train_label_distribution
	return train_label_distribution
def get_train_label_distribution(i):
	global train_label_distribution
	return train_label_distribution[i]	
def set_train_label_distribution(new_train_label_distribution):
	global train_label_distribution
	train_label_distribution = new_train_label_distribution
def append_train_label_distribution(new_train_label_distribution):
	global train_label_distribution
	train_label_distribution.append(new_train_label_distribution)	
def increment_train_label_distribution(i):
	global train_label_distribution
	train_label_distribution[i] = train_label_distribution[i] + 1		

test_label_distribution = []
def get_all_test_label_distribution():
	global test_label_distribution
	return test_label_distribution
def get_test_label_distribution(i):
	global test_label_distribution
	return test_label_distribution[i]	
def set_test_label_distribution(new_test_label_distribution):
	global test_label_distribution
	test_label_distribution = new_test_label_distribution
def append_test_label_distribution(new_test_label_distribution):
	global test_label_distribution
	test_label_distribution.append(new_test_label_distribution)
def increment_test_label_distribution(i):
	global test_label_distribution
	test_label_distribution[i] = test_label_distribution[i] + 1			

generation_detection_rate_sum = 0
def get_generation_detection_rate_sum():
	global generation_detection_rate_sum
	return generation_detection_rate_sum
def set_generation_detection_rate_sum(new_generation_detection_rate_sum):
	global generation_detection_rate_sum
	generation_detection_rate_sum = new_generation_detection_rate_sum

generation_distance_sum = 0
def get_generation_distance_sum():
	global generation_distance_sum
	return generation_distance_sum
def set_generation_distance_sum(new_generation_distance_sum):
	global generation_distance_sum
	generation_distance_sum = new_generation_distance_sum

generation_score_sum = 0
def get_generation_score_sum():
	global generation_score_sum
	return generation_score_sum
def set_generation_score_sum(new_generation_score_sum):
	global generation_score_sum
	generation_score_sum = new_generation_score_sum

generation_detection_rate_average = []
def get_generation_detection_rate_average():
	global generation_detection_rate_average
	return generation_detection_rate_average
def set_generation_detection_rate_average(new_generation_detection_rate_average):
	global generation_detection_rate_average
	generation_detection_rate_average = new_generation_detection_rate_average
def append_generation_detection_rate_average(new_generation_detection_rate_average):
	global generation_detection_rate_average
	generation_detection_rate_average.append(new_generation_detection_rate_average)	

generation_distance_average = []
def get_generation_distance_average():
	global generation_distance_average
	return generation_distance_average
def set_generation_distance_average(new_generation_distance_average):
	global generation_distance_average
	generation_distance_average = new_generation_distance_average
def append_generation_distance_average(new_generation_distance_average):
	global generation_distance_average
	generation_distance_average.append(new_generation_distance_average)

generation_score_average = []
def get_generation_score_average():
	global generation_score_average
	return generation_score_average
def set_generation_score_average(new_generation_score_average):
	global generation_score_average
	generation_score_average = new_generation_score_average
def append_generation_score_average(new_generation_score_average):
	global generation_score_average
	generation_score_average.append(new_generation_score_average)	