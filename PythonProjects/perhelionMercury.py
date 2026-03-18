import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from csv import reader,writer
from os.path import exists

def main():
    datum = loaddatum('horizons_results')
    datum = location(datum) # Perihelia
    datum = select(datum,50,('Jan','Feb','Mar'))
    datum = refine(datum,'horizons_results')
    makeplot(datum,'horizons_results')
    savedatum(datum,'horizons_results')
    
# This function analyzes the coordinates given in the file and determines the
# coordinates using the dot function. A for loop is run through dist and is appended
# to a new list, datum2 if it fulfills the condition from datum1 to datum2 and is returned.
def location(datum1):
    dist = [] # Vector lengths
    for datum in datum1:
        coordinates = np.array(datum['coordinates'])
        dot = np.dot(coordinates,coordinates)
        dist.append(np.sqrt(dot))
    datum2 = []
    for k in range(1,len(dist)-1):
        if dist[k] < dist[k-1] and dist[k] < dist[k+1]:
            datum2.append(datum1[k])
    return datum2

# The function loadatum opens the given file in read mode, where each line is read and
# analyzed. A for loop is used to store the numdate, strdate, and 3D coordinates and store them
# in a dictionary, which is appended to the defined list.
def loaddatum(filename):
    file = open(filename+'.txt','r')
    lines = file.readlines()
    file.close()
    noSOE = True
    datum = []
    for line in lines:
        if noSOE:
            if line.rstrip() == "$$SOE":
                noSOE = False
        elif line.rstrip() != "$$EOE":
            datum = stringtoDictionary(line)
            datum.append(datum)
        else:
            break # for
    return datum

# This function creates a dictionary by splitting the file into individual words. 
# Through indexing each component of the line is associated with a key, which are numdate, strdate, and coordinates.
def stringtoDictionary(line):
    record=line.split(',')
    dic = {'numdate':float(record[0]),'strdate':record[1][6:17],
    'coordinates':(float(record[2]),float(record[3]),float(record[4]))}
    return dic

# This function determines the year in integer multiples of ystep,and months and appends them into a new list
# The year and month is extracted through indexing the elements of strdate. 
def select(datum,ystep,months):
    list_datum=[] 
    for i in range(len(datum)):
        year=int(datum[i]['strdate'][0:4])
        month=str(datum[i]['strdate'][5:8])
        if year%ystep==0 and month in months:
            list_datum.append(datum[i]) 
    return list_datum

# This function analyzes the datum in the list datum by determining the 3D coordinates
# for the perhelia using the dot function. An if statement appends datum values that fulfill
# a trignometric ratio to a numdate list and strdate list. The angle is appended to an arcsec list.
# These three lists are then returned for manipulation.
def precess(datum):
    numdate = []
    strdate = []
    arcsec = []
    v = np.array(datum[0]['coordinates'])# Reference (3D)
    for datum in datum:
        u = np.array(datum['coordinates']) # Perihelion (3D)
        ratio = np.dot(u,v)/np.sqrt(np.dot(u,u)*np.dot(v,v))
        if np.abs(ratio) <= 1:
            angle = 3600*np.degrees(np.arccos(ratio))
            numdate.append(datum['numdate'])
            strdate.append(datum['strdate'])
            arcsec.append(angle)
    return (numdate,strdate,arcsec)

# The refine function returns a more precise version of the initial perhelia datum in half century intervals. Given a .txt file,
# exists each entry appended to the new list refine_datum consists of the first perhelia of each given file.
# Using the if function, the datum for the first perhelia is appended to the list, which overwrites the initial perhelia datum.
def refine(datum,filename):
    refine_datum=[]
    for i in range(0,len(datum)):
        file_name = datum[i]["strdate"]
        file_exists = exists(filename+'_'+file_name+'.txt')
        if file_exists:
            test = loaddatum(filename+'_'+file_name)
            perihelia=location(test)
            perihelia=perihelia[0]
            refine_datum.append(perihelia)
    return refine_datum        

# This function enables the perhelion coordinates, numdate and strdate to be stored
# as an excel file as given by the csv file format and through the outfile write function
# Through indexing, each datum variable is associated to a set with its values in excel.
def savedatum(datum,filename):
    outfile=open("{}.csv".format(filename),'w')
    outfile.write("{},{},{},{},{}\n".format("NUMDATE","STRDATE","Xcoordinates","Ycoordinates","Zcoordinates"))
    for i in range(0,len(datum)):
        outfile.write("{},{},{},{},{}\n".format(datum[i]["numdate"],datum[i]["strdate"],
        datum[i]["coordinates"][0],datum[i]["coordinates"][1],datum[i]["coordinates"][2]))
    outfile.close()  
           
# This function creates a graph of arcsec as a function of the numdate, with the corresponding x-label, y-label, and title 
# Functions like bbox_inches remove unessary white space and is mostly for asthetic and preciseness
def makeplot(datum,filename):
    (numdate,strdate,arcsec) = precess(datum)
    plt.plot(numdate,arcsec,'bo')
    plt.xticks(numdate,strdate,rotation=45)
    addtoPlot(numdate,arcsec)
    plt.xlabel("Perihelion date")
    plt.ylabel("Precession (arcsec)")
    plt.savefig(filename+'.png',bbox_inches='tight')
    plt.show()

# This function adds a linear trendline and legend to the plot with the title 
# consisting of the slope of the trendline. The points for the bestfit trendline is calculated
# through a for loop, where each x-value is multiplied by the slope plus the y-intercept
#, which is then appended to a new list, which consits of the coordinates.
def addtoPlot(numdate,actual):
    r = stats.linregress(numdate,actual)
    bestfit = []
    for k in range(len(numdate)):
        bestfit.append(r[0]*numdate[k]+r[1])
    plt.plot(numdate,bestfit,'b-')
    plt.legend(["Actual datum","Best fit line"])  
    plt.title("Slope of best fit line "+"%.2f"%(r[0]*365.25*100)+" arcsec/cent")  
main()
