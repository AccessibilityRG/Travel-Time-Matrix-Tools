# -*- coding: cp1252 -*-
import sys, os
import pandas as pd
import numpy as np

#Methods

class Iterator:
    def __init__(self):

        #Constructor
        self.code = ''
        self.count = 0

    def cumulativeSum(self, row, sumColumn, dependent):
        """Calculates a cumulative sum of sumColumn if value belongs to the same group as earlier value (based on dependent column), if not restarts the calculation"""
        if row[dependent] != self.code:
            self.code = row[dependent]
            self.count=row[sumColumn]   #Clear count value
            return self.count
        else:
            self.count+=row[sumColumn] #Make cumulative sum
            return self.count

#Filepaths
#.........

#Travel times (Origin-Destination) for all selected cells
Path = r'...\Travel_times_from_chosen_originIDs_to_selected_destinationIDs.txt'

#Hockey players within YKR-cells --> Changes made in xlsx: Column names were changed, and total number were deleted from the end of the file.
PlayerCount = r'...\Kiekkoilijat_ruutu.xlsx'

#----------------------------------
#Read files and clean them
#----------------------------------

Ykr = pd.read_csv(Path, sep=';')
PlrCnt = pd.read_excel(PlayerCount)

#Combine Travel times data and Player count data by doing a join (Key: YKR_id, JoinType: 'outer')
data = Ykr.merge(PlrCnt, left_on='from_id', right_on='YKR_id', how='outer')

#Change -1 values to NaN
data = data.replace(to_replace={'Walk_time': {-1: np.nan}, 'Walk_dist': {-1: np.nan},'PT_total_time': {-1: np.nan},'PT_time': {-1: np.nan}, 'PT_dist': {-1: np.nan},
                                'Car_time': {-1: np.nan}, 'Car_dist': {-1: np.nan}})

#Take only data that has no NaN values (worthless) --> there were in total 3 cells with NoData
data = data.dropna(subset=['Walk_time','Car_time','PT_total_time'])

#Drop dublicate column (YKR_id)
data = data.drop(labels=['YKR_id'], axis=1)

#----------------------------------
#Determine closest sport facility for each origin cell
#----------------------------------

#Group by 'from_id' (i.e. cell of SLU member)
grouped = data.groupby('from_id')

#Create empty DataFrame for results of each transportation mode
PT = pd.DataFrame()
Car = pd.DataFrame()
Walk = pd.DataFrame()

#Iterate over the grouped items (i.e. member-cells) and determine the closest facility for each travel mode (walk, PT, car)
for group in grouped:

    #Find closest facility by Public transportation
    PTcol = group[1]['PT_total_time']
    PTclosest = group[1][PTcol == int(PTcol.min())]
    PT = PT.append(PTclosest[['from_id', 'to_id', 'PT_total_time', 'PT_dist', 'Count']])

    #Find closest facility by Car
    carCol = group[1]['Car_time']
    carClosest = group[1][carCol == int(carCol.min())]
    Car = Car.append(carClosest[['from_id', 'to_id', 'Car_time', 'Car_dist', 'Count']])

    #Find closest facility by Walking
    walkCol = group[1]['Walk_time']
    walkClosest = group[1][walkCol == int(walkCol.min())]
    Walk = Walk.append(walkClosest[['from_id', 'to_id', 'Walk_time', 'Walk_dist', 'Count']])

#----------------------------------
#Determine distance decay for each sport facility by different travel modes
#----------------------------------

#Public Transportation
#---------------------

#Sort values by travel time
PTsort = PT.sort(columns='PT_total_time')

#Group by 'to_id' (i.e. closest sport facility) and by time-distance (i.e. cells that are same time-distance apart from the facility
grouped = PTsort.groupby(by=['to_id','PT_total_time'])

#Create empty dataframe for distance decay values
PTdecay = pd.DataFrame()

for group in grouped:

    #Sum the members that are same time-distance apart from the facility
    members = group[1]['Count'].sum()

    #Calculate average distance from origin cells to destination (i.e. from home locations to sport facility)
    avgDist = int(group[1]['PT_dist'].mean())

    #Other necessary values
    from_id, to_id, time = group[1]['from_id'].values[0], group[1]['to_id'].values[0], group[1]['PT_total_time'].values[0]

    #Append these to results
    PTdecay = PTdecay.append([[from_id,to_id,time,avgDist,members]])

#Add column names
PTdecay.columns=['from_id', 'to_id', 'PT_total_time', 'PT_avg_dist', 'Member_count']

#Create an instance of Iterator class
Iter = Iterator()

#Calculate cumulative sum of members
PTdecay['Members_cum'] = PTdecay.apply(Iter.cumulativeSum, axis=1, sumColumn='Member_count', dependent='to_id')

#Calculate cumulative sum of distance
PTdecay['Dist_cum'] = PTdecay.apply(Iter.cumulativeSum, axis=1, sumColumn='PT_avg_dist', dependent='to_id')


#------------------------------------------------------------------------

#Private Car
#---------------------

#Sort values by travel time
carSort = Car.sort(columns='Car_time')

#Group by 'to_id' (i.e. closest sport facility) and by time-distance (i.e. cells that are same time-distance apart from the facility
grouped = carSort.groupby(by=['to_id','Car_time'])

#Create empty dataframe for distance decay values
carDecay = pd.DataFrame()

for group in grouped:

    #Sum the members that are same time-distance apart from the facility
    members = group[1]['Count'].sum()

    #Calculate average distance from origin cells to destination (i.e. from home locations to sport facility)
    avgDist = int(group[1]['Car_dist'].mean())

    #Other necessary values
    from_id, to_id, time = group[1]['from_id'].values[0], group[1]['to_id'].values[0], group[1]['Car_time'].values[0]

    #Append these to results
    carDecay = carDecay.append([[from_id,to_id,time,avgDist,members]])

#Add column names
carDecay.columns=['from_id', 'to_id', 'Car_total_time', 'Car_avg_dist', 'Member_count']

#Create an instance of Iterator class
Iter = Iterator()

#Calculate cumulative sum of members
carDecay['Members_cum'] = carDecay.apply(Iter.cumulativeSum, axis=1, sumColumn='Member_count', dependent='to_id')

#Calculate cumulative sum of distance
carDecay['Dist_cum'] = carDecay.apply(Iter.cumulativeSum, axis=1, sumColumn='Car_avg_dist', dependent='to_id')

#------------------------------------------------------------------------

#Walking
#---------------------

#Sort values by travel time
walkSort = Walk.sort(columns='Walk_time')

#Group by 'to_id' (i.e. closest sport facility) and by time-distance (i.e. cells that are same time-distance apart from the facility
grouped = walkSort.groupby(by=['to_id','Walk_time'])

#Create empty dataframe for distance decay values
walkDecay = pd.DataFrame()

for group in grouped:

    #Sum the members that are same time-distance apart from the facility
    members = group[1]['Count'].sum()

    #Calculate average distance from origin cells to destination (i.e. from home locations to sport facility)
    avgDist = int(group[1]['Walk_dist'].mean())

    #Other necessary values
    from_id, to_id, time = group[1]['from_id'].values[0], group[1]['to_id'].values[0], group[1]['Walk_time'].values[0]

    #Append these to results
    walkDecay = walkDecay.append([[from_id,to_id,time,avgDist,members]])

#Add column names
walkDecay.columns=['from_id', 'to_id', 'Walk_time', 'Walk_avg_dist', 'Member_count']

#Create an instance of Iterator class
Iter = Iterator()

#Calculate cumulative sum of members
walkDecay['Members_cum'] = walkDecay.apply(Iter.cumulativeSum, axis=1, sumColumn='Member_count', dependent='to_id')

#Calculate cumulative sum of distance
walkDecay['Dist_cum'] = walkDecay.apply(Iter.cumulativeSum, axis=1, sumColumn='Walk_avg_dist', dependent='to_id')


#-----------------------------------------------------------
# Write outputs --> to Csv
#-----------------------------------------------------------

folderPath = r'...\TravelTimes'

#Public Transportation
PTdecay.to_csv(os.path.join(folderPath, "IceHockey_distanceDecay_PublicTransport.txt"), sep=';', index=False)

#Private Car
carDecay.to_csv(os.path.join(folderPath, "IceHockey_distanceDecay_Car.txt"), sep=';', index=False)

#Walking
walkDecay.to_csv(os.path.join(folderPath, "IceHockey_distanceDecay_Walk.txt"), sep=';', index=False)

