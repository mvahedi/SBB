# Fall-Winter 2016 
__author__ = 'Maryam Vahedi'
###############################################################
###UTILS
###############################################################
from config import *

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
    new_host_population = []
    print '****** removing similar teams in generation: ', get_generation()
    print 'number of teams: ', len(get_host_population())
    i = 0
    for first_team in get_host_population():
        j = i + 1
        is_duplicate = False
        while j < len(get_host_population()):
            if get_host_population()[i] == get_host_population()[j]:
                is_duplicate = True
                break
            j = j + 1
        if not is_duplicate:
            new_host_population.append(first_team)
        i= i + 1
    set_host_population(new_host_population[:])
    print 'number of unique teams: ', len(get_host_population())      


def clean_symbionts():
    set_host_population(flatten(get_host_population()))
    set_host_population([i for i in get_host_population() if i is not None])
    delete_symbiont_population()
    for i in get_host_population():
        team_symbionts = i.getSymbionts()
        for s in team_symbionts:
            if s not in get_symbiont_population():
                append_symbiont_population(s) 
    clean_instruction_population()   

def clean_instruction_population():
    set_symbiont_population(flatten(get_symbiont_population()))
    set_symbiont_population([i for i in get_symbiont_population() if i is not None])
    delete_instruction_population()
    for i in get_symbiont_population():
        program_instructions = i.getInstructions()
        for s in program_instructions:
            if s not in get_instruction_population():
                append_instruction_population(s)        
