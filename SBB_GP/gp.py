# Fall-Winter 2016 
__author__ = 'Maryam Vahedi'
###############################################################
### CALCULATION
###############################################################
from config import *
from util import *
from init import *
from variation import *
from write import *

def checkGeneration():
    teams_are_good = False
    set_host_population(flatten(get_host_population()))
    print len(get_host_population())
    if get_host_population()[len(get_host_population())-1].getScore() >= getMIN_TEAM_SCORE():
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

def rank_teams(isTest = False, isAll = False):
    if isTest:
        print '****** Ranking Teams with Test data - DATA COUNT: ', get_test_data_count()
        rankData = get_test_data()
    elif isAll:
        print '****** Ranking Teams with All data - DATA COUNT: ', get_data_count()
        rankData = get_data()
    else:
        print '****** Ranking Teams with Training data - DATA COUNT: ', get_train_data_count() 
        rankData = get_train_data() 

    set_host_population(flatten(get_host_population()))

    for host in get_host_population():
        host.resetTeam()

    for exemplar in rankData:
        for host in get_host_population():
            host.evaluate_team(exemplar)

    for host in get_host_population():
        host.calculateDetectionRates(isTest, isAll)

    sort_host_population()

    for host in get_host_population():
        host.resetTeam()

    for exemplar in rankData:
        isDetected = False;
        label = getLABELS().index(exemplar[getLABEL_INDEX()])
        for host in get_host_population():
            isCorrect = host.evaluate_team(exemplar)
            if isCorrect or isDetected:
                acc = host.getAccumulativeCorrectCount(label) + 1
                host.setAccumulativeCorrectCount(label, acc)
                isDetected = True              

    host_id = 1            
    for host in get_host_population():
        host_id = host_id + 1
        host.calculateDetectionRates(isTest, isAll)
        index = 0
        while index < getLABEL_COUNT():
            print host_id , " " , host.getCorrectCount(index) , " " , host.getAccumulativeCorrectCount(index)
            index = index + 1 
        print host_id , " " , host.getTeamDetectionRate() , " " , host.getAccumulativeDetectionRate()            

    #Calculate team distances
    for host in get_host_population():
        host_average_distance = 0
        for other_host in get_host_population(): 
            host_average_distance = host_average_distance + calculateTeamDistance(host, other_host)
        host_average_distance = Decimal(host_average_distance / get_host_population_length())
        host.setDistance(host_average_distance)  
        host.calculateScore()     

def evaluate_teams():
    optimal_detection_rate_reached = False
    print "****** Evaluating ", get_host_population_length(), " teams ******"
    extend_host_population(get_new_teams())
    delete_parent_host_population()
    remove_similar_teams()
    rank_teams()
    set_host_population(flatten(get_host_population()))
    set_host_population([i for i in get_host_population() if i is not None])
    sort_by_score_host_population()
    printTeams()  
    return checkGeneration()

def calculate_generation_average():
    set_generation_detection_rate_sum(0)
    set_generation_distance_sum(0)
    set_generation_score_sum(0)
    j = 0
    for host in get_host_population(): 
        set_generation_detection_rate_sum(get_generation_detection_rate_sum()+host.getTeamDetectionRate())
        set_generation_distance_sum(get_generation_distance_sum()+host.getDistance())
        set_generation_score_sum(get_generation_score_sum()+host.getScore())
        j = j + 1
    append_generation_detection_rate_average(get_generation_detection_rate_sum()/get_host_population_length())
    append_generation_distance_average(get_generation_distance_sum()/get_host_population_length()) 
    append_generation_score_average(get_generation_score_sum()/get_host_population_length())


def selectParents():
    #Select parent teams
    delete_parent_host_population()
    parent_count = int(len(get_host_population()) * getPOPULATION_PARENT_RATE())
    parent_indexes = random.sample(range(0, len(get_host_population())-1), parent_count)
    for i in parent_indexes:
        append_parent_host_population(get_host_population()[i])
    set_parent_host_population(flatten(get_parent_host_population()))
    print "****** Parent population: ", len(get_parent_host_population())
    j = 0
    for host in get_parent_host_population(): 
        print 'Team: ', j, 'Team Action: ' ,host.getAction(), ' Team Score: ', host.getScore()
        j = j + 1  

def run_gp():
    print '****** Initial host population size: ', len(host_population)
    stop_criteria_met = False
    while (stop_criteria_met == False):
        set_generation(get_generation()+1)
        optimal_detection_rate_reached = evaluate_teams()
        # Only save results for every 10 generation
        if get_generation() == 1 or get_generation() % getSAVE_GENERATIONS() == 0 or optimal_detection_rate_reached:
            saveGenerationResults()
        # Last generation    
        if get_generation() == getMAX_ALLOWABLE_GENERATIONS() or optimal_detection_rate_reached:
            stop_criteria_met = True
            print "****** FINAL TEAMS: "
            rank_teams(True)
            saveGenerationResults(True)
            rank_teams(False, True)
            saveGenerationResults(False, True)
            printTeams()
        else: 
            cleanup()   
            selectParents()
            evolve_teams()   
        calculate_generation_average()

    print 'Total number of generations: ', get_generation()
    saveAverageResults()
