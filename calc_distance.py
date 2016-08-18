import os

import googlemaps 
from googlemaps.convert import as_list

google_api_key = os.environ["GOOGLE_MAPS_SERVER_API_KEY"]

gmaps = googlemaps.Client(key=google_api_key)

def find_distance(origin, dests, units="imperial"):
    """call distance_matrix API to get distance between startpt and each of the locations"""

    distance_matrix_driving = gmaps.distance_matrix(origin, dests, units="imperial")
    # distance_matrix_transit = gmaps.distance_matrix(origin, dests, units="imperial", mode="transit")
    # distance_matrix_walking = gmaps.distance_matrix(origin, dests, units="imperial", mode="walking")
    
    return distance_matrix_driving



# def compare_distance():
#     """compare distances to point_0(starting point), based on distance function"""

#     distance = find_distance(origin, dests, units="imperial") #call distance function to get dictionary
#     next_stop = min(distance, key=distance.get)
#     return point_1


def parse_dict(d):
    """parse dictionary to read results from returned distance_matrix api python call"""

    
    for key, value in d.items():
        # print key, value
        print key, value
    return key, value
