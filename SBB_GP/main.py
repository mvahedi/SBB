# Fall-Winter 2016 
__author__ = 'Maryam Vahedi'
###############################################################
###START
###############################################################
#from read import *
from init import initiate_teams
from gp import run_gp

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
    selection=raw_input("Please Select:") 
    if selection =='1': 
      print "Iris data selected" 
    elif selection == '2': 
      print "Thyroid data selected"
    elif selection == '3':
      print "Shuttle data selected" 
    elif selection == '4': 
      print "Exiting GP"  	
      return
    else: 
      print "Unknown Option Selected!" 

get_user_input()
#read_data()
#initiate_teams()
#run_gp()

###############################################################
###END
###############################################################