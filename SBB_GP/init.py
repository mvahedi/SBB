# Fall-Winter 2016 
__author__ = 'Maryam Vahedi'
###############################################################
###INITIALIZE
###############################################################
from config import *
from class_def import *
from gene import *
from variation import *
from util import *

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
    p = 0
    while p < INSTRUCTION_POP_SIZE:
        new_instruction = generate_instructions()
        if new_instruction not in get_instruction_population():
            append_instruction_population(new_instruction)  
            p = p + 1        

def initiate_symbiont_population():
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
            instruction.append(get_instruction_population()[program_instructions[i]])
            i = i + 1
        symbiont_action = random.randint(0, LABEL_COUNT-1)
        ind =  symbiont(instruction, symbiont_action)
        symbionts.append(ind)
        p = p + 1
        print "Symbiont:  ", p, " Action: ", symbiont_action , " # of instructions: ", number_of_instructions_in_program, " instruction Length: ", len(instruction)
    return symbionts

def initiate_teams():
    set_symbiont_population(initiate_symbiont_population())
    i = 0
    while i < TEAM_COUNT:
        symbionts = []
        symbiont_count_in_team = random.randint(MIN_TEAM_SIZE, MAX_TEAM_SIZE)
        team_symbionts = random.sample(range(0, INSTRUCTION_POP_SIZE-1), symbiont_count_in_team)
        p = 0
        for symbiont in team_symbionts:
            symbionts.append(get_symbiont_population()[team_symbionts[p]])
            p = p + 1       
        multyActionTeam(symbionts)
        t =  team(symbionts)
        host_population.append(t)
        i = i + 1
    clean_symbionts() 