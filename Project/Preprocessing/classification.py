import pandas as pd
import numpy as np

def get_gini( videogames_data, att, attributes, global_sales ):
    gini = 0.0
    for attribute in attributes:
        n = len( videogames_data[ videogames_data[att] == attribute ] )
        for sale in global_sales:
            p = len( videogames_data[ (videogames_data[att] == attribute) & (videogames_data["Nominal_Global_Sales"] == sale) ] )
            gini += (p/float(n))*( 1 - p/float(n) ) 
    return gini

def check_attribute( attribute, n, x ):
    if( attribute == "Developer" ): return n >= x*0.15
    if( attribute == "Publisher" ): return n >= x*0.15
    return True

def get_videogames( videogames_data, att, lis ):
    r = []
    for videogames in videogames_data:
        for val in lis:
            print( att, val )
            r.append( videogames[ videogames[att] == val ] )
    return r


videogames_data = pd.read_csv("complete_processed_nominal_videogames_data.csv")

videogames_data.drop("Name",1, inplace=True )
videogames_data.drop("Critic_Count",1, inplace=True )
videogames_data.drop("Critic_Score",1, inplace=True )
videogames_data.drop("EU_Sales",1, inplace=True )
videogames_data.drop("Global_Sales",1, inplace=True )
videogames_data.drop("JP_Sales",1, inplace=True )
videogames_data.drop("NA_Sales",1, inplace=True )
videogames_data.drop("Other_Sales",1, inplace=True )
videogames_data.drop("User_Count",1, inplace=True )
videogames_data.drop("User_Score",1, inplace=True )
videogames_data.drop("Nominal_EU_Sales",1, inplace=True )
videogames_data.drop("Nominal_JP_Sales",1, inplace=True )
videogames_data.drop("Nominal_NA_Sales",1, inplace=True )
videogames_data.drop("Nominal_Other_Sales",1, inplace=True )

#print( videogames_data )

global_sales = videogames_data["Nominal_Global_Sales"].unique()

nominal_user_score = sorted( videogames_data["Nominal_User_Score"].unique() )

lines = []
with open("input") as f:
   for line in f:
        lines.append( line )
        if 'str' in line:
            break

j = 0
for i in xrange( len(lines)/2 ):
    line = lines[j].strip("\n")
    attributes = line.split(',')

    line = lines[j+1].strip("\n")
    values = line.split(",")

    j += 2

    videogames = videogames_data
    for att,val in zip( attributes, values ):
        videogames = videogames[ videogames[att] == val ]

    print( "---------------------------------------------------" )
    print attributes
    print values
    print videogames
    print( "---------------------------------------------------" )
    print
    raw_input()

'''
critic = "Worst"
user = "Worst"
rating = "T"
genre = "Action"
developer = "Capcom"
publisher = "Ubisoft"

videogames_data = videogames_data[ (videogames_data["Nominal_Critic_Score"] == critic) & (videogames_data["Nominal_User_Score"] == user) ]

print videogames_data

print( videogames_data[ "Developer" ].unique() )
print( videogames_data[ "Publisher" ].unique() )
print( videogames_data[ "Nominal_Global_Sales" ].unique() )
'''

'''
videogames_data = get_videogames( [videogames_data], "Nominal_Critic_Score", sorted( videogames_data["Nominal_Critic_Score"].unique() ) )
videogames_data = get_videogames( videogames_data, "Nominal_User_Score", nominal_user_score )
attributes = [ "Developer", "Genre", "Publisher", "Rating", "Year_of_Release" ]
'''

'''
attributes = [ "Developer", "Genre", "Publisher", "Rating", "Year_of_Release" ]

videogames_data = [videogames_data]

for i, videogames in enumerate( videogames_data ):
    for att in attributes:
        keys = videogames[att].unique()
        lis = []
        print att, 
        for k in keys: 
            n = len( videogames[ videogames[att] == k ] )
            if( check_attribute( att, n, len(keys) ) ):
                lis.append( k )
        lis = sorted(lis)
        print lis
        print
        print( i, att, get_gini( videogames, att, lis, global_sales ) )
'''

'''
critics = videogames_data["Nominal_Critic_Score"].unique()

print( len(critics) )

lis = []
for critic in critics:
    lis.append( ( critic, len( videogames_data[ videogames_data["Nominal_Critic_Score"] == critic ] ) ) )

lis = sorted(lis, key=lambda x: -x[1])

print(lis)


cnt = 0
for e in lis:
    if( e[1] >= 44 ):
        cnt += 1
print(cnt)
'''
