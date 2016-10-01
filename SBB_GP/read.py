###############################################################
###READ DATA
###############################################################
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
    


#This function reads the iris data from the csv file
def read_data(): 
    global data
    global data_count
    global train_data
    global test_data
    global label_disctribution

    selection = get_user_input()
    if selection =='1': 
          print "Iris data selected"
          LABELS = ['Iris-setosa', 'Iris-versicolor', 'Iris-virginica']
          LABEL_COUNT = len(LABELS)
          LABEL_INDEX = 4
          DATA_DELIMITER = ',' 
          file_name = 'iris.csv'
        elif selection == '2': 
          print "Thyroid data selected"
        elif selection == '3':
          print "Shuttle data selected" 
        elif selection == '4': 
          print "Exiting GP"    
          return
        else: 
          print "Unknown Option Selected!"
          return

    with open(filename) as data_file:
        for line in data_file:
            data.append(line.strip().split(DATA_DELIMITER))
    
    data_count = len(data)
    index = 0
    while index < LABEL_COUNT:
        label_disctribution.append(0)
        index = index + 1
    for exemplar in data:
        i = 0
        for label in LABELS:
            if exemplar[LABEL_INDEX] == label:
                label_disctribution[i] = label_disctribution[i] + 1
            i = i + 1    
    i = 0 
    for label in LABELS:
        print "ALL # of rows in class: ", label, " is ", label_disctribution[i]
        i = i + 1
    
    random.shuffle(data) 
    training_count = int(data_count * TRAINING_PERCENT / 100)

    train_data = data[:training_count]
    train_data_count = len(train_data)
    print 'traning count ', train_data_count

    index = 0
    while index < LABEL_COUNT:
        train_label_disctribution.append(0)
        index = index + 1
    for exemplar in train_data:
        i = 0
        for label in LABELS:
            if exemplar[LABEL_INDEX] == label:
                train_label_disctribution[i] = train_label_disctribution[i] + 1
            i = i + 1    
    i = 0 
    for label in LABELS:
        print "TRAIN # of rows in class: ", label, " is ", train_label_disctribution[i]
        i = i + 1

    test_data = data[training_count:]  
    test_data_count = len(test_data)
    print 'test count ', test_data_count

    index = 0
    while index < LABEL_COUNT:
        test_label_disctribution.append(0)
        index = index + 1
    for exemplar in test_data:
        i = 0
        for label in LABELS:
            if exemplar[LABEL_INDEX] == label:
                test_label_disctribution[i] = test_label_disctribution[i] + 1
            i = i + 1    
    i = 0 
    for label in LABELS:
        print "TEST: # of rows in class: ", label, " is ", test_label_disctribution[i]
        i = i + 1  