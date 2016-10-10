# Fall-Winter 2016 
__author__ = 'Maryam Vahedi'
###############################################################
### WRITE
###############################################################
from config import *

def printTeams():
    j = 0
    for host in get_host_population(): 
        print 'Team: ', j, 'Team Action: ' ,host.getAction(), ' Detection Rate: ', host.getTeamDetectionRate(), ' Accumulative Detection Rate: ', host.getAccumulativeDetectionRate(), ' Distance: ', host.getDistance() , ' # of active symbionts: ', len(host.getActiveSymbionts()), ' SCORE: ', host.getScore()
        j = j + 1

def saveGenerationResults(isTest = False, isAll = False):
    generation_results = []
    sort_host_population()
    for i in range(len(get_host_population())): 
        host = get_host_population()[i]       
        generation_results.append({"Host":i,"TeamAction":host.getAction(),
            "DetectionRate":host.getTeamDetectionRate(),
            "AccumulativeDetectionRate":host.getAccumulativeDetectionRate(),
            "ErrorRate":host.getTeamErrorRate(),
            "AccumulativeErrorRate":host.getAccumulativeErrorRate(),
            "Distance":host.getDistance(),
            "ActiveSymbiontCount":len(host.getActiveSymbionts()),"Score":host.getScore()})
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
        filename = directory + 'genration' + str(get_generation()) + '.csv'            
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


def saveAverageResults():
    average_results = []
    i = 1
    for i in range(get_generation()):
        print 'Generation: ', i, ' average detection rate: ', get_generation_detection_rate_average()[i], ' average distance: ', get_generation_distance_average()[i], ' average score: ', get_generation_score_average()[i]
        average_results.append({"Generation":i,"average detection rate":get_generation_detection_rate_average()[i],
            "average distance":get_generation_distance_average()[i],
            "average score":get_generation_score_average()[i]})
        i += 1
    directory = os.path.join('results/')
    if not os.path.exists(os.path.dirname(directory)):
        try:
            os.makedirs(os.path.dirname(directory))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
    filename = directory + "GenerationAverages.csv"                        
    try:
        fp = open(filename)
    except IOError:
        # If not exists, create the file
        fp = open(filename, 'wb')
        
    print "writing to file: ", filename
    headings = ['Generation','average detection rate','average distance','average score']   
    with fp as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(headings)
        for row in average_results:
            wr.writerow([row['Generation'],row['average detection rate']
                , row['average distance'], row['average score']]) 
