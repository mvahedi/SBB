# Fall-Winter 2016 
__author__ = 'Maryam Vahedi'
###############################################################
###VARIATION
###############################################################
from config import *

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