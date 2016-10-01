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
        filename = directory + "Test_Data.csv"
    elif isAll == True:
        filename = directory + "All_Data.csv"    
    else:               
        filename = directory + 'genration' + str(generation) + '.csv'            
    try:
        fp = open(filename)
    except IOError:
        # If not exists, create the file
        fp = open(filename, 'wb')
        
    print "writing to file: ", filename
    headings = ['Host','TeamAction','DetectionRate', 'AccumulativeDetectionRate','ErrorRate', 'AccumulativeErrorRate',"Distance",'ActiveSymbiontCount','Score']   
    with fp as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(headings)
        for row in generation_results:
            wr.writerow([row['Host'],row['TeamAction']
                , row['DetectionRate'], row['AccumulativeDetectionRate']
                , row['ErrorRate'], row['AccumulativeErrorRate']
                , row["Distance"],row['ActiveSymbiontCount'],row['Score']]) 