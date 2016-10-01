
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

def cleanup():
    if len(host_population) > TEAM_COUNT:
        #Remove the bad teams botom 20%
        delete_count = len(host_population) - TEAM_COUNT
        delete_count = delete_count + int(len(host_population) * POPULATION_REMOVAL_RATE)
        del host_population[-delete_count:]
        print "AFTER REMOVING ", delete_count, " TEAMS: ", len(host_population)
    clean_symbionts()

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
