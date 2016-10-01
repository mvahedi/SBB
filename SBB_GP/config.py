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
LABELS = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
LABEL_COUNT = len(LABELS)
DATA_DELIMITER = ','
OPERATORS = ['+', '-', '*', '/', 'cos', 'ln', 'exp', 'if']
OP_COUNT = len(OPERATORS)
LABEL_INDEX = 4

INSTRUCTION_POP_SIZE        = 100 
SYMBIONT_POP_SIZE           = 500
PROGRAM_MIN_INSTRUCTIONS    = 2
PROGRAM_MAX_INSTRUCTIONS    = 48
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


### Number of times to try before we give up
MAX_ALLOWABLE_GENERATIONS   = 50
MIN_TEAM_SCORE = 0.85

### genotypic configurations
TARGET_COUNT = 2
SOURCE_COUNT = 4
MODE_BIT_COUNT = 1
OP_BIT_COUNT = 3
TARGET_BIT_COUNT = 1
SOURCE_BIT_COUNT = 2
ENCODED_BIT_COUNT = MODE_BIT_COUNT + OP_BIT_COUNT + TARGET_BIT_COUNT + SOURCE_BIT_COUNT
ENCODED_DECIMAL_EQUIVELANT = 2 ** ENCODED_BIT_COUNT
SAVE_GENERATIONS = 5

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

generation_detection_rate_sum = 0
generation_distance_sum = 0
generation_score_sum = 0
generation_detection_rate_average = []
generation_distance_average = []
generation_score_average = []