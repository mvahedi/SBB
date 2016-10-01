###############################################################
### CALCULATION
###############################################################

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

def rank_teams(isTest = False, isAll = False):
    global host_population
    global data_count
    global train_data_count
    global test_data_count
    global data
    global test_data
    global train_data 

    if isTest:
        print '****** Ranking Teams with Test data - DATA COUNT: ', test_data_count
        rankData = test_data
    elif isAll:
        print '****** Ranking Teams with All data - DATA COUNT: ', data_count
        rankData = data
    else:
        print '****** Ranking Teams with Training data - DATA COUNT: ', train_data_count 
        rankData = train_data 

    host_population = flatten(host_population)

    for host in host_population:
        host.resetTeam()

    for exemplar in rankData:
        for host in host_population:
            host.evaluate_team(exemplar)

    for host in host_population:
        host.calculateDetectionRates(isTest, isAll)

    host_population.sort(key = lambda i: i.getTeamDetectionRate(), reverse=True)

    for host in host_population:
        host.resetTeam()

    for exemplar in rankData:
        isDetected = False;
        label = LABELS.index(exemplar[LABEL_INDEX])
        for host in host_population:
            isCorrect = host.evaluate_team(exemplar)
            if isCorrect or isDetected:
                acc = host.getAccumulativeCorrectCount(label) + 1
                host.setAccumulativeCorrectCount(label, acc)
                isDetected = True              

    host_id = 1            
    for host in host_population:
        host_id = host_id + 1
        host.calculateDetectionRates(isTest, isAll)
        index = 0
        while index < LABEL_COUNT:
            print host_id , " " , host.getCorrectCount(index) , " " , host.getAccumulativeCorrectCount(index)
            index = index + 1 
        print host_id , " " , host.getTeamDetectionRate() , " " , host.getAccumulativeDetectionRate()            

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
    rank_teams()
    host_population = flatten(host_population)
    host_population = [i for i in host_population if i is not None]
    host_population.sort(key = lambda i: i.getScore(), reverse=True)
    printTeams()  
    return checkGeneration()

def calculate_generation_average():
    global generation_detection_rate_sum
    global generation_distance_sum
    global generation_score_sum
    global generation_detection_rate_average
    global generation_distance_average
    global generation_score_average
    generation_detection_rate_sum = 0
    generation_distance_sum = 0
    generation_score_sum = 0
    j = 0
    for host in host_population: 
        generation_detection_rate_sum+=host.getTeamDetectionRate()
        generation_distance_sum+=host.getDistance()
        generation_score_sum+=host.getScore()
        j = j + 1
    generation_detection_rate_average.append(generation_detection_rate_sum/len(host_population)) 
    generation_distance_average.append(generation_distance_sum/len(host_population)) 
    generation_score_average.append(generation_score_sum/len(host_population))  


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

def run_gp():
    global generation
    global symbiont_population
    global host_population
    global generation_detection_rate_sum
    global generation_score_sum
    global generation_detection_rate_average
    global generation_score_average
    print '****** Initial host population size: ', len(host_population)
    stop_criteria_met = False
    while (stop_criteria_met == False):
        generation+=1
        optimal_detection_rate_reached = evaluate_teams()
        # Only save results for every 10 generation
        if generation == 1 or generation % SAVE_GENERATIONS == 0 or optimal_detection_rate_reached:
            saveGenerationResults()
        # Last generation    
        if generation == MAX_ALLOWABLE_GENERATIONS or optimal_detection_rate_reached:
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

    print 'Total number of generations: ', generation
    i = 1
    for i in range(generation):
        print 'Generation: ', i, " average detection rate: ", generation_detection_rate_average, " average score: ", generation_score_average
        i += 1
