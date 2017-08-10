# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 19:35:06 2016

@author: daniel
"""
#==============================================================================
# Algorithm
#     repeatedly asks the user to put in a file name until a valid one is given,
#         this program is intended to work with State_Data.csv,
#         State_Data.csv is a file containing economic data on U.S. states
#     reads the content of the file into a dictionary;
#     displays the extreme values for GDP per capita and Per capita income of 
#         the chosen region and economic data for every state in the region;
#     allows user to choose two economic values (as x and y) to plot a 
#         regression line between the values for each state in the region.     
#==============================================================================
   
import matplotlib.pyplot as plt
import numpy as np

REGION_LIST = ["far_west","great_lakes","mideast","new_england","plains",\
    "rocky_mountain", "southeast","southwest","all"]

MAP_LIST = ["Pop", "GDP", "PI", "Sub", "CE", "TPI", "GDPp", "PIp"]
    
def open_file():
    '''
    Opens file for reading.
    parameters: none
    returns: a pointer to the file
    '''
    inp = input("Please enter a valid file name:")
    
    while True: #iterate until correct file (State_Data.csv) is opened
        try:
            file = open(inp,"r")   #open file for reading
            return file
            
        except IOError:   #input/output error
            print("File could not be found")
            inp = input("Please enter a valid file name:")


def read_to_dict(file):
    '''
    Fills a newly created dictionary with states as the keys and a list of
        economic elements as the values.
    Also prints the extreme values for GDP per capita and per capita personal
        income and the states associated with those values.
    parameter: file, the file pointer found in the open_file() function
    returns: d, the dictionary, filled with state data in the respective region
    '''
    
    d = dict()
    title = file.readline() #holds first line of file
    title = title.strip()
    title = title.split(",")
    print()
    
    print("These are the valid regions in the United States")
        
    for item in REGION_LIST: #print each region
        if item != REGION_LIST[-1]:
            print(item.capitalize(), end = ", ")
        else:
            print(item.capitalize())
            
    reg = input("Choose a valid region to search from:")

    while reg.lower() not in REGION_LIST:
        #account for combination of upper and lower case letters
        print("Invalid region name!")
        reg = input("Choose a valid region to search from:")
        
    reg = reg.lower() #lower case letters

    #obtain extreme values for GDP per capita and Per capita income
    highGDPper = 0
    highGDPstate = ""
    lowGDPper = 1000000
    lowGDPstate = ""
    
    highPIper = 0
    highPIstate = ""
    lowPIper = 1000000
    lowPIstate = ""
           
    for line in file: #read through file pointer
        line = line.strip() #clear \n at end
        line = line.split(",") #split list based on commas
        name = line[0] #name of state
        region = line[1] #region of state
          
        if region.lower() == reg or reg.lower() == "all":
            d[name] = [line[1]]
            ln = [round(float(i),2) for i in line[2:]]
            d[name].extend(ln) 
            #change all values, besides region and state from string, to float

            GDPpC = round(((ln[1] * 1000) /ln[0]),2) #GDP per capita
            PIpC = round(((ln[2] * 1000) /ln[0]),2) #Per capita income
        
            d[name].append(GDPpC) #GDP per capita
            d[name].append(PIpC) #Per capita income    

            if (d[name][7]) > highGDPper: #hgih GDP per capita
                highGDPper = (d[name][7])
                highGDPstate = name
                
            if (d[name][7]) < lowGDPper: #low GDP per capita
                lowGDPper = (d[name][7])
                lowGDPstate = name
                
            if (d[name][8]) > highPIper: #high per capita income
                highPIper = (d[name][8])
                highPIstate = name
                
            if (d[name][8]) < lowPIper: #low per capita income
                lowPIper = d[name][8]
                lowPIstate = name
    
    print()   #spacing
    if reg == "all":
        print ("Looking in the United States")
    else:
        print("Looking in the {:s} region".format(reg.title()))
        
    print()   #spacing
    print("{} has the highest GDP per capita at ${:,.2f} per person"\
    .format(highGDPstate,highGDPper))

    print("{} has the lowest GDP per capita at ${:,.2f} per person"\
    .format(lowGDPstate,lowGDPper))
    
    print()   #spacing

    print("{} has the highest PI per capita at ${:,.2f} per person"\
    .format(highPIstate,highPIper))

    print("{} has the lowest PI per capita at ${:,.2f} per person"\
    .format(lowPIstate,lowPIper))
    
    print()   #spacing
    print()   #spacing
    
    print("All states in this region:")
    print()   #spacing
    print("{:<15} {:<15} {:<13} {:<13} {:<13} {:<12} {:<13} {:<13} {:<13} {:<13}"
        .format("State", "Region", "Population(m)", "GDP(b)", "PI(b)","Sub(m)", 
          "COE(b)", "TPI(b)", "GDPp", "PIp"))
    
    
    for itr in d: #iterate through the region dictionary
    
        prstr = "{:<15} {:<15} {:<13,} ${:<12,} ${:<12,} ${:<12,}"
        prstr += "${:<12,} ${:<12,} ${:<12,} ${:<12,}"
        
        print(prstr.format(itr,d[itr][0],\
        d[itr][1],d[itr][2],d[itr][3],d[itr][4],\
        d[itr][5],d[itr][6],d[itr][7],d[itr][8]))
          
    return d


def plotting(dreg):
    '''
    Plot x and y values for each state in the selected region
    parameters: dreg: a dictionary containing the states of the selected region
    return: nohting is returned, but a scatter plot is graphed
    '''
    
    print()   #spacing
    print ("Choose x and y list values from the following:")
    print ("Pop, GDP, PI, Sub, CE, TPI, GDPp, PIp")
    xstr = input("Enter x-axis list:")
    ystr = input("Enter y-axis list:")
    
    while xstr not in MAP_LIST or ystr not in MAP_LIST:
        #user can plot the same value against itself
        print("Please choose a correct x and y list to plot")
        print("Pop, GDP, PI, Sub, CE, TPI, GDPp, PIp")
        
        xstr = input("Enter x-axis list:")
        ystr = input("Enter y-axis list:")
    
    x_pos = MAP_LIST.index(xstr)+1
    y_pos = MAP_LIST.index(ystr)+1
    #plus 1 because first item for each key in dreg is region name
        #ex:index        0   1   2
            #MAP_LIST:  Pop GDP PI
            #dreg[key]: Reg Pop GDP
    
    x_new = [] #list of x values for each state in region
    y_new = [] #list of y....
    State = [] #list of state names corresponding to same x and y
    
    print() #spacing
    print("{:<15} {:<9} {:<9}".format("",xstr,ystr))
    for i in dreg:  #obtain each value for each state in the region
        x_new.append(dreg[i][x_pos])
        y_new.append(dreg[i][y_pos])
        State.append(i)
        print("{:<15} {:<9} {:<9}".format(i,dreg[i][x_pos],dreg[i][y_pos]))

    #print("For {:s}, values of x_new:".format(xstr),x_new)
    #print("For {:s}, values of y_new:".format(ystr),y_new)
    
    xarr = np.array(x_new) #numpy array
    yarr = np.array(y_new) #numpy arry 
    
    plt.figure(figsize = (7,7))   #figure size
    plt.title(xstr + " vs " + ystr)   #title
    
    plt.xlabel(xstr)   #label x axis
    plt.ylabel(ystr)   #label y axis
    plt.scatter(xarr,yarr)   #create the scatter plots
    
    for i, txt in enumerate(State): #label points with state names
        plt.annotate(txt, (x_new[i],y_new[i]))

    m,b = np.polyfit(xarr,yarr, deg = 1) #creates slope and intercept for
        #linear graph, only takes numpy arrays as parameters
    plt.plot(xarr,m*xarr + b, '-') #plots the regression line
        
    plt.grid()   #add a grid
    plt.show()   #shows graph on python console
            

def main():   #main function
    fp = open_file()
    
    ADict = read_to_dict(fp)
    
    plotting(ADict)

if __name__ == "__main__":
    main()