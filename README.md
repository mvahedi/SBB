Directed Studies Project Winter 2016 - Implementing Symbiotic Bid-Based GP

How to run:

To run create results folder in the same directory as py file

python 2.7 (and higher)

python name_of_file.py

example:

python SBB_Iris.py


Configurations:

The configuration parameters are the the very top of the python files. The values are set for the three datasets used in this project but they can be adjusted easily to work with a new dataset. The config values for Thyroid dataset is explained below:

******************************************* initialization config
LABELS = ['1','2','3'] 					*** classes
LABEL_COUNT = len(LABELS) 				*** number of classes
DATA_DELIMITER = ' ' 					*** data delimiter used 
OPERATORS = ['+', '-', '*', '/', 'cos', 'ln', 'exp', 'if']
OP_COUNT = len(OPERATORS)				*** number of operators
LABEL_INDEX = 21						*** the index of the label column in the dataset

INSTRUCTION_POP_SIZE        = 50	  	*** number of instructions generated during initialization
SYMBIONT_POP_SIZE           = 200		*** number of symbionts generated during initialization
PROGRAM_MIN_INSTRUCTIONS    = 1	  		*** minimum number of instructions in each symbiont	
PROGRAM_MAX_INSTRUCTIONS    = 5			*** maximum number of instructions in each symbiont	
TRAINING_PERCENT            = 70		*** percentage of data used for training (only used for Iris)
RELATIVE_NOVELTY_WEIGHT     = 0.5		*** novelty weight used in calculating team scores

TEAM_COUNT                  = 50		*** number of teams (hosts) in each generation
MONOLITHIC                  = False		*** monolithic teams not implemented yet 
MIN_TEAM_SIZE               = 2			*** minimum number of symbionts in each team
MAX_TEAM_SIZE               = 10		*** maximum number of symbionts in each team
POPULATION_REMOVAL_RATE     = 0.20		*** percentage of teams removed in each generation
POPULATION_PARENT_RATE      = POPULATION_REMOVAL_RATE
										*** percentage of teams selected as parents in each generation

******************************************* Rates for Variation Operators
TEAM_ADD_RATE               = 0.7		
TEAM_DELETE_RATE            = 0.7
SYMBIONT_MODIFICATION_RATE  = 0.2
SYMBIONT_ACTION_CHANGE_RATE = 0.1
ADD_INSTRUCTION_RATE        = 0.5
DELETE_INSTRUCTION_RATE     = 0.5
INSTRUCTION_MUTATION_RATE   = 0.1
INSTRUCTION_SWAP_RATE       = 0.1
LABEL_SAMPLE_COUNT          = 20


MAX_ALLOWABLE_GENERATIONS   = 250		*** maximum number of generations
MIN_TEAM_SCORE = 0.85					*** end condition - This may need to be changed
SAVE_GENERATIONS = 5					*** multiple of generation results will be saved to file 

******************************************* genotypic configurations
TARGET_COUNT = 4
SOURCE_COUNT = 21
MODE_BIT_COUNT = 1
OP_BIT_COUNT = 3
TARGET_BIT_COUNT = 2
SOURCE_BIT_COUNT = 5
ENCODED_BIT_COUNT = MODE_BIT_COUNT + OP_BIT_COUNT + TARGET_BIT_COUNT + SOURCE_BIT_COUNT
ENCODED_DECIMAL_EQUIVELANT = 2 ** ENCODED_BIT_COUNT
