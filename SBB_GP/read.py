# Fall-Winter 2016 
__author__ = 'Maryam Vahedi'
###############################################################
###READ DATA
###############################################################
from config import *

filename = 'iris.csv'
trnfilename = ''
testfilename = ''

def get_user_input():
    menu = {}
    menu['1']="Iris" 
    menu['2']="Thyroid"
    menu['3']="Shuttle"
    menu['4']="Exit"
    options=menu.keys()
    options.sort()
    for entry in options: 
        print entry, menu[entry]
    return raw_input("Please Select:") 
 

def read_data():
    global filename
    global trnfilename
    global testfilename
    selection = get_user_input()
    has_test_data = 'false'
    if selection =='1': 
        print "Iris data selected"
        setLABELS(['Iris-setosa', 'Iris-versicolor', 'Iris-virginica'])
        setLABEL_INDEX(4)
        setDATA_DELIMITER(',') 
        filename ='iris.csv'
        setTARGET_COUNT(2)
        setSOURCE_COUNT(4)
        setTARGET_BIT_COUNT(1)
        setSOURCE_BIT_COUNT(2)
    elif selection == '2':
        print "Thyroid data selected"
        setLABELS(['1','2','3'])
        setDATA_DELIMITER(' ')
        setLABEL_INDEX(21)
        testfilename = "ann-test.data"
        trnfilename = "ann-train.data"
        has_test_data = 'true'
        setTARGET_COUNT(4)
        setSOURCE_COUNT(21)
        setTARGET_BIT_COUNT(2)
        setSOURCE_BIT_COUNT(5)
    elif selection == '3':
        print "Shuttle data selected" 
        setLABELS(['1','2','3','4','5','6','7'])
        setDATA_DELIMITER(',')
        setLABEL_INDEX(9)
        testfilename = "shuttle_test.data"
        trnfilename = "shuttle_trn.data"
        has_test_data = 'true'
        setTARGET_COUNT(8)
        setSOURCE_COUNT(9)
        setTARGET_BIT_COUNT(3)
        setSOURCE_BIT_COUNT(4)
    elif selection == '4': 
        print "Exiting GP"    
        exit()
    else: 
        print "Unknown Option Selected!"
        exit()
    if has_test_data == 'false':
        read_all_data()
    else:    
        read_data_file()
        sample_data()
        read_test_data()


#This function reads the iris data from the csv file
def read_data_file(): 
    global trnfilename
    print '****** Reading Data ... '
    with open(trnfilename) as data_file:
        for line in data_file:
            append_data(line.strip().split(getDATA_DELIMITER()))

    index = 0
    while index < getLABEL_COUNT():
        append_label_distribution(0)
        index = index + 1
    for exemplar in get_data():
        i = 0
        for label in getLABELS():
            if exemplar[getLABEL_INDEX()] == label:
                increment_label_distribution(i)
            i = i + 1    

    i = 0 
    for label in getLABELS():
        print "All # of rows in class: ", label, " is ", get_label_distribution(i)
        i = i + 1
    print '****** Reading DONE!'          

def sample_data(): 
    set_train_data([])
    set_train_label_distribution([])
    print '****** Sampling Data ... '
    index = 0
    while index < getLABEL_COUNT():
        append_train_label_distribution(0)
        index = index + 1
    for exemplar in get_random_data():
        i = 0
        for label in getLABELS():
            if exemplar[getLABEL_INDEX()] == label:
                if get_train_label_distribution()[i] < getLABEL_SAMPLE_COUNT():
                    append_train_data(exemplar)
                    increment_train_label_distribution(i)
            i = i + 1    

    i = 0 
    for label in getLABELS():
        while get_train_label_distribution()[i] < getLABEL_SAMPLE_COUNT():
            for exemplar in get_random_data():
                if exemplar[getLABEL_INDEX()] == label:
                    if get_train_label_distribution()[i] < getLABEL_SAMPLE_COUNT():
                        append_train_data(exemplar)
                        increment_train_label_distribution(i)
        print "Sampling ", get_train_label_distribution()[i] ," rows in class: ", label, " out of ", get_label_distribution(i)
        i = i + 1

    print "Train Data Count ", get_train_data_count()
    print '****** Sampling DONE!' 

def read_test_data(): 
    global testfilename
    with open(testfilename) as data_file:
        for line in data_file:
            append_test_data(line.strip().split(getDATA_DELIMITER()))
    
    print "Test Data Count ", get_test_data_count()
    index = 0
    while index < getLABEL_COUNT():
        append_test_label_distribution(0)
        index = index + 1
    for exemplar in test_data:
        i = 0
        for label in getLABELS():
            if exemplar[getLABEL_INDEX()] == label:
                increment_test_label_distribution(i)
            i = i + 1    
    i = 0 
    for label in getLABELS():
        print "ALL # of rows in class for test data: ", label, " is ", get_test_label_distribution(i)
        i = i + 1  

def read_train_data(): 
    global trnfilename
    train_label_distribution = []
    train_data = []
    with open(trnfilename) as data_file:
        for line in data_file:
            append_train_data(line.strip().split(getDATA_DELIMITER()))
    print "All training Data Count ", get_train_data_count()
    index = 0
    while index < getLABEL_COUNT():
        append_train_label_distribution(0)
        index = index + 1
    for exemplar in train_data:
        i = 0
        for label in getLABELS():
            if exemplar[getLABEL_INDEX()] == label:
                increment_train_label_distribution(i)
            i = i + 1    
    i = 0 
    for label in getLABELS():
        print "ALL # of rows in class for training data: ", label, " is ", get_train_label_distribution(i)
        i = i + 1         

#This function reads the iris data from the csv file
def read_all_data(): 
    global filename
    with open(filename) as data_file:
        for line in data_file:
            append_data(line.strip().split(getDATA_DELIMITER()))
    
    index = 0
    while index < getLABEL_COUNT():
        append_label_distribution(0)
        index = index + 1
    for exemplar in data:
        i = 0
        for label in getLABELS():
            if exemplar[getLABEL_INDEX()] == label:
                increment_label_distribution(i)
            i = i + 1    
    i = 0 
    for label in getLABELS():
        print "ALL # of rows in class: ", label, " is ", get_label_distribution(i)
        i = i + 1
    
    training_count = int(get_data_count() * getTRAINING_PERCENT() / 100)
    set_train_data(get_random_data()[:training_count])
    print 'traning count ', get_train_data_count()

    index = 0
    while index < getLABEL_COUNT():
        append_train_label_distribution(0)
        index = index + 1
    for exemplar in get_train_data():
        i = 0
        for label in getLABELS():
            if exemplar[getLABEL_INDEX()] == label:
                increment_train_label_distribution(i)
            i = i + 1    
    i = 0 
    for label in getLABELS():
        print "TRAIN # of rows in class: ", label, " is ", get_train_label_distribution(i)
        i = i + 1

    set_test_data(get_data()[training_count:])  
    print 'test count ', get_test_data_count()

    index = 0
    while index < getLABEL_COUNT():
        append_test_label_distribution(0)
        index = index + 1
    for exemplar in get_test_data():
        i = 0
        for label in getLABELS():
            if exemplar[getLABEL_INDEX()] == label:
                increment_test_label_distribution(i)
            i = i + 1    
    i = 0 
    for label in getLABELS():
        print "TEST: # of rows in class: ", label, " is ", get_test_label_distribution(i)
        i = i + 1  