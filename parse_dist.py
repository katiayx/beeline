"""helper functions: once input is received, data is organized and sent via API
call to get distance information. Once API results are returned, functions to 
help parse data into final dictionary to be jsonified"""

import os
import googlemaps
from googlemaps import convert

google_api_key = os.environ["GOOGLE_MAPS_SERVER_API_KEY"]
gmaps = googlemaps.Client(key=google_api_key)


def get_lists(locations):
    """create origin-destination lists for API call


    user input is a list of locations. Need to create dictionary key:pairs pairs
    for each location as origin, and rest as destinations.

        >>> get_lists(['Portland, OR', 'Vancouver, WA', 'Troutdale'])
        {'Vancouver, WA': ['Portland, OR', 'Troutdale'], 'Portland, OR': ['Vancouver, WA', 'Troutdale'], 'Troutdale': ['Portland, OR', 'Vancouver, WA']}

    """

    location_dict = {}
    for origin in locations:
        location_dict[origin] = []
        for destination in locations:
            if destination != origin:
                location_dict[origin].append(destination)
            else:
                pass

    return location_dict
    #O(n^3)


def get_api_distance(location_dict):
    """Unpack location_dict dictionary, and bind 'origin' to the key, and 'dests'
    to the value. Distance matrix API call takes 3 parameters: origin, dests, and units. 
    'Origin' and 'Dests' can be string, a list or geocodes. API call returns a 
    dictionary with nested list of dictionaries.

    """

    list_distances = []
    for pair in location_dict.items():
        origin = pair[0]
        dests = pair[1]
        result = gmaps.distance_matrix(origin, dests, units="imperial")
        list_distances.append(result)

    return list_distances
    #O(n) - unpacking
    #O(1) - list append
    #ttl: O(n)


def parse_results_distance(list_distances):
    """API call returned results include additional information besides just a 
    distance number. Since origin, dests, and distance are not grouped together, 
    need to parse each into individual lists to be concatnated later.

    list_distances is the raw result returned by API call.

        
        >>> list_distances = [{u'status': u'OK', 
        ...     u'rows': 
        ...          [{u'elements': 
        ...               [{u'duration': {u'text': u'55 mins', u'value': 3323}, 
        ...               u'distance': {u'text': u'52.8 mi', u'value': 84987}, 
        ...               u'status': u'OK'}, 
        ...               {u'duration': {u'text': u'45 mins', u'value': 2725}, 
        ...               u'distance': {u'text': u'38.0 mi', u'value': 61138}, 
        ...               u'status': u'OK'}]}],
        ...     u'origin_addresses': [u'Alameda, CA, USA'], 
        ...     u'destination_addresses': [u'Vacaville, CA, USA', u'San Jose, CA, USA']}, 
        ...     {u'status': u'OK', u'rows': 
        ...         [{u'elements': 
        ...               [{u'duration': {u'text': u'55 mins', u'value': 3324}, 
        ...               u'distance': {u'text': u'52.8 mi', u'value': 84915}, 
        ...               u'status': u'OK'}, 
        ...               {u'duration': {u'text': u'1 hour 24 mins', u'value': 5029}, 
        ...               u'distance': {u'text': u'86.9 mi', u'value': 139790}, 
        ...               u'status': u'OK'}]}], 
        ...     u'origin_addresses': [u'Vacaville, CA, USA'], 
        ...     u'destination_addresses': [u'Alameda, CA, USA', u'San Jose, CA, USA']}, 
        ...     {u'status': u'OK', u'rows': 
        ...         [{u'elements': 
        ...               [{u'duration': {u'text': u'1 hour 25 mins', u'value': 5082}, 
        ...               u'distance': {u'text': u'86.8 mi', u'value': 139638}, 
        ...               u'status': u'OK'}, 
        ...               {u'duration': {u'text': u'47 mins', u'value': 2828}, 
        ...               u'distance': {u'text': u'38.0 mi', u'value': 61087}, 
        ...               u'status': u'OK'}]}], 
        ...     u'origin_addresses': [u'San Jose, CA, USA'], 
        ...     u'destination_addresses': [u'Vacaville, CA, USA', u'Alameda, CA, USA']}]

        >>> parse_results_distance(list_distances)
        [52.8, 38.0, 52.8, 86.9, 86.8, 38.0]

    """

    distance_list = []
    for di in list_distances: #O(n)
        new_di = di['rows'][0]['elements'] #O(1)
        for di in new_di: #O(n)
            distance = di['distance']['text'] #O(1)
            if ',' in distance:
                distance = distance.replace(',', '')
            distance_list.append(distance)
    distance_list = [str(i) for i in distance_list]
    distance_list = [i.rstrip(' mi') for i in distance_list]
    distance_list = [float(i) for i in distance_list]

    return distance_list
    #O(n^2)


def parse_results_origin(list_distances):
    """parse API results to pull list of origins


        >>> list_distances = [{u'status': u'OK', 
        ...     u'rows': 
        ...          [{u'elements': 
        ...               [{u'duration': {u'text': u'55 mins', u'value': 3323}, 
        ...               u'distance': {u'text': u'52.8 mi', u'value': 84987}, 
        ...               u'status': u'OK'}, 
        ...               {u'duration': {u'text': u'45 mins', u'value': 2725}, 
        ...               u'distance': {u'text': u'38.0 mi', u'value': 61138}, 
        ...               u'status': u'OK'}]}],
        ...     u'origin_addresses': [u'Alameda, CA, USA'], 
        ...     u'destination_addresses': [u'Vacaville, CA, USA', u'San Jose, CA, USA']}, 
        ...     {u'status': u'OK', u'rows': 
        ...         [{u'elements': 
        ...               [{u'duration': {u'text': u'55 mins', u'value': 3324}, 
        ...               u'distance': {u'text': u'52.8 mi', u'value': 84915}, 
        ...               u'status': u'OK'}, 
        ...               {u'duration': {u'text': u'1 hour 24 mins', u'value': 5029}, 
        ...               u'distance': {u'text': u'86.9 mi', u'value': 139790}, 
        ...               u'status': u'OK'}]}], 
        ...     u'origin_addresses': [u'Vacaville, CA, USA'], 
        ...     u'destination_addresses': [u'Alameda, CA, USA', u'San Jose, CA, USA']}, 
        ...     {u'status': u'OK', u'rows': 
        ...         [{u'elements': 
        ...               [{u'duration': {u'text': u'1 hour 25 mins', u'value': 5082}, 
        ...               u'distance': {u'text': u'86.8 mi', u'value': 139638}, 
        ...               u'status': u'OK'}, 
        ...               {u'duration': {u'text': u'47 mins', u'value': 2828}, 
        ...               u'distance': {u'text': u'38.0 mi', u'value': 61087}, 
        ...               u'status': u'OK'}]}], 
        ...     u'origin_addresses': [u'San Jose, CA, USA'], 
        ...     u'destination_addresses': [u'Vacaville, CA, USA', u'Alameda, CA, USA']}]

        >>> parse_results_origin(list_distances)
        ['Alameda, CA, USA', 'Vacaville, CA, USA', 'San Jose, CA, USA']

    """

    origin_list = []
    for o in list_distances:
        origin = o['origin_addresses']
        origin_list.append(origin)
    origin_list = [str(o[0]) for o in origin_list]

    return origin_list
    #O(n)


def parse_results_dests(list_distances):
    """parse API results to pull nested list of dests


        >>> list_distances = [{u'status': u'OK', 
        ...     u'rows': 
        ...          [{u'elements': 
        ...               [{u'duration': {u'text': u'55 mins', u'value': 3323}, 
        ...               u'distance': {u'text': u'52.8 mi', u'value': 84987}, 
        ...               u'status': u'OK'}, 
        ...               {u'duration': {u'text': u'45 mins', u'value': 2725}, 
        ...               u'distance': {u'text': u'38.0 mi', u'value': 61138}, 
        ...               u'status': u'OK'}]}],
        ...     u'origin_addresses': [u'Alameda, CA, USA'], 
        ...     u'destination_addresses': [u'Vacaville, CA, USA', u'San Jose, CA, USA']}, 
        ...     {u'status': u'OK', u'rows': 
        ...         [{u'elements': 
        ...               [{u'duration': {u'text': u'55 mins', u'value': 3324}, 
        ...               u'distance': {u'text': u'52.8 mi', u'value': 84915}, 
        ...               u'status': u'OK'}, 
        ...               {u'duration': {u'text': u'1 hour 24 mins', u'value': 5029}, 
        ...               u'distance': {u'text': u'86.9 mi', u'value': 139790}, 
        ...               u'status': u'OK'}]}], 
        ...     u'origin_addresses': [u'Vacaville, CA, USA'], 
        ...     u'destination_addresses': [u'Alameda, CA, USA', u'San Jose, CA, USA']}, 
        ...     {u'status': u'OK', u'rows': 
        ...         [{u'elements': 
        ...               [{u'duration': {u'text': u'1 hour 25 mins', u'value': 5082}, 
        ...               u'distance': {u'text': u'86.8 mi', u'value': 139638}, 
        ...               u'status': u'OK'}, 
        ...               {u'duration': {u'text': u'47 mins', u'value': 2828}, 
        ...               u'distance': {u'text': u'38.0 mi', u'value': 61087}, 
        ...               u'status': u'OK'}]}], 
        ...     u'origin_addresses': [u'San Jose, CA, USA'], 
        ...     u'destination_addresses': [u'Vacaville, CA, USA', u'Alameda, CA, USA']}]

        >>> parse_results_dests(list_distances)
        [['Vacaville, CA, USA', 'San Jose, CA, USA'], ['Alameda, CA, USA', 'San Jose, CA, USA'], ['Vacaville, CA, USA', 'Alameda, CA, USA']]
    """

    dests_list = []
    for d in list_distances:
        dest = d['destination_addresses']
        dests_list.append(dest)
    dests_list = [[str(i) for i in d] for d in dests_list]

    return dests_list
    #O(n)


def concat_dest_dist(distance_list, dests_list):
    """ Match up dests_list and distance_list: 
        - create same number of sublists as dests_list
        - add each element into a new list, but new list length should be the 
        same as dests_list

        >>> distance_list = [9.9, 20.9, 9.0, 16.0, 16.6, 20.9]
        >>> dests_list = [['Portland, OR, USA', 'Troutdale, OR 97060, USA'],
        ...     ['Vancouver, WA, USA', 'Troutdale, OR 97060, USA'],
        ...     ['Portland, OR, USA', 'Vancouver, WA, USA']]

        >>> concat_dest_dist(distance_list, dests_list) 
        [[('Portland, OR, USA', 9.9), ('Troutdale, OR 97060, USA', 20.9)], [('Vancouver, WA, USA', 9.0), ('Troutdale, OR 97060, USA', 16.0)], [('Portland, OR, USA', 16.6), ('Vancouver, WA, USA', 20.9)]]

    """

    i = 0
    chunk = len(dests_list[0])
    ordered_dist = []
    while i < len(distance_list):
        ordered_dist.append(distance_list[i: i+chunk])
        i += chunk
    dest_dist_list = []
    for j in range(len(dests_list)):
        dest_dist_list.append(zip(dests_list[j], ordered_dist[j]))

    return dest_dist_list
    #O(n)



def sort_distance(dest_dist_list):
    """given a list of (dest, distance)list of tuples, sort by miles so 
    tuple with smallest mileage appears first


        >>> dest_dist_list = [[('Troutdale, OR 97060, USA', 20.9), ('Portland, OR, USA', 9.9)],
        ...     [('Troutdale, OR 97060, USA', 16.0), ('Vancouver, WA, USA', 9.0)],
        ...     [('Vancouver, WA, USA', 20.9), ('Portland, OR, USA', 16.6)]]

        >>> sort_distance(dest_dist_list)
        [[('Portland, OR, USA', 9.9), ('Troutdale, OR 97060, USA', 20.9)], [('Vancouver, WA, USA', 9.0), ('Troutdale, OR 97060, USA', 16.0)], [('Portland, OR, USA', 16.6), ('Vancouver, WA, USA', 20.9)]]
    
    """

    sorted_dest_dist_list = []
    for tup_list in dest_dist_list:
        s = sorted(tup_list, key=lambda y: y[1])
        sorted_dest_dist_list.append(s)
    
    return sorted_dest_dist_list
    #O(n)


def concat_origin_dest_dist(origin_list, sorted_dest_dist_list):
    """create a dictionary with origin as key, list of dest/mi tuples as value


        >>> origin_list = ['Vancouver, WA, USA', 'Portland, OR, USA', 'Troutdale, OR 97060, USA']
        >>> sorted_dest_dist_list = [[('Portland, OR, USA', 9.9), ('Troutdale, OR 97060, USA', 20.9)],
        ...     [('Vancouver, WA, USA', 9.0), ('Troutdale, OR 97060, USA', 16.0)],
        ...     [('Portland, OR, USA', 16.6), ('Vancouver, WA, USA', 20.9)]]

        >>> concat_origin_dest_dist(origin_list, sorted_dest_dist_list)
        {'Vancouver, WA, USA': [('Portland, OR, USA', 9.9), ('Troutdale, OR 97060, USA', 20.9)], 'Troutdale, OR 97060, USA': [('Portland, OR, USA', 16.6), ('Vancouver, WA, USA', 20.9)], 'Portland, OR, USA': [('Vancouver, WA, USA', 9.0), ('Troutdale, OR 97060, USA', 16.0)]}

    """

    raw_list = zip(origin_list, sorted_dest_dist_list)
    origin_dest_dist_dict = dict(raw_list)
    
    return origin_dest_dist_dict
    #O(n^2)


def get_origin_stop(locations):
    """ """

    origin = locations[0]
    result = gmaps.geocode(origin)
    start = str(result[0]['formatted_address'])

    return start
    #O(1)
    
def order_stops(start, origin_dest_dist_dict):
    """create a list of ordered stops, initially add only locations[0]
    which is the first element in the original user-input list, because that's 
    always going to be the start point. Then iterate through origin_dest_dist_dict
    to grab the remaining stops

        >>> start = 'Portland, OR, USA'
        >>> origin_dest_dist_dict = {'Vancouver, WA, USA': [('Portland, OR, USA', 9.9), ('Troutdale, OR 97060, USA', 20.9)],
        ...     'Troutdale, OR 97060, USA': [('Portland, OR, USA', 16.6), ('Vancouver, WA, USA', 20.9)],
        ...     'Portland, OR, USA': [('Vancouver, WA, USA', 9.0), ('Troutdale, OR 97060, USA', 16.0)]}
        
        >>> order_stops(start, origin_dest_dist_dict)
        ['Portland, OR, USA', 'Vancouver, WA, USA', 'Troutdale, OR 97060, USA']
    
    """

    # grab origin from user_input, match with api result string, append to stops list
    stops = []
    #make start the first item in stops list
    stops.append(start)

    # while stops list is shorter than concanated dictionary, go thought each stop
    while len(stops) < len(origin_dest_dist_dict):
        for stop in stops: #O(n)
            # if city in stop is in dictionary, then new variable dests is 
            if stop in origin_dest_dist_dict: #O(1)
                # equal to the values of dict[city]
                dests = origin_dest_dist_dict[stop] #O(1)
                # iterate through values - list of tuples
                for tup in dests: #O(n)
                    # add tuple at city index to stops list if city is not in stops list
                    if tup[0] not in stops: #O(1)
                        next_stop = tup[0]
                        stops.append(next_stop)

    
    return stops
    #O(n^2)


###################################################################################################################################
# DOCTESTS

if __name__ == "__main__":
    from doctest import testmod
    if testmod().failed == 0:
        app.debug = True

        