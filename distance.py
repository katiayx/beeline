
from math import sqrt

point_0 = list(raw_input("Starting from:"))#starting point for route plotting
#turn user input into a list of coordinates

#How to convert user input into lat-long - to be explored

locations = raw_input("Where do you want to go?")#grab locations from user input
location_list = locations.split()#split locations based on tbd, and output
#location list
a, b, c, d = location_list #unpack the list to grab individual 
#locations

def distance():
    """calculate distance between each location and point_0, and store
    {a: distance} as a dictionary

    results should look like:
    {a: 5}
    """

    point_dist = {}
    for point in location_list:
        distance = sqrt(sum([pow(point_0 - point, 2) for point_0, point in pairs]))
        #get actual distance from Google Maps. How to make the call to get that
        point_dist[point] = distance
    return point_dist

    #permutation of all possible routes between two points???


def compare_distance():
    """compare distances to point_0(starting point), based on distance function"""

    point_dist = distance() #call distance function to get dictionary
    point_1 = min(point_dist, key=point_dist.get)
    return point_1

#wraps up calculation for first location: now I need to tell the app to plot 
#point_0 to point_1 - not there yet.

#next location: point_2
point_1 = compare_distance()
point_dist = del point_dist[point_1]

#repeat distance and compare_distance functions









