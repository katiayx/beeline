
import os
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
import googlemaps
from googlemaps import convert
import json

google_api_key = os.environ["GOOGLE_MAPS_SERVER_API_KEY"]  
gmaps = googlemaps.Client(key=google_api_key)
mykey = os.environ["GOOGLE_MAPS_BROWSER_API_KEY"]


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route("/")
def index():
    """display homepage"""

    return render_template("homepage.html",
                            mykey=mykey)



@app.route('/distance', method=['POST'])
def get_list_locations():
    """get value from user input form, filter out any empty input"""

    locations = request.forms.get("locations") 
    locations = filter(None, locations)
    

    location_dict = get_api_distances(locations)
    list_distances = get_distance(location_dict)
    distance_list = parse_results_distance(list_distances)
    origin_list = parse_results_origin(list_distances)
    dests_list = parse_results_dests(list_distances)
    dest_dist_list = concat_dest_dist(distance_list, dests_list)
    sorted_dest_dist_list = sort_distance(dest_dist_list)
    origin_dest_dist_dict = concat_origin_dest_dist(origin_list, sorted_dest_dist_list)
    stops = order_waypts(origin_list, origin_dest_dist_dict)
    stops_d = get_json(stops)


    return render_template('/route_map.html',
                            stops_d=stops_d,
                            mykey=mykey)

    # return jsonify (stops_d)
    # #{'origin': 0, 'stop1': 1, 'stop2': 2...}



def get_api_distances(locations):
    """create origin-destination lists for API call"""
 
    location_dict = {}
    for origin in locations:
        location_dict[origin] = []
        for destination in locations:
            if destination != origin:
                location_dict[origin].append(destination)
            else:
                pass
    
    print location_dict
    return location_dict


def get_distance(location_dict):
    """Make distance API call for all combinations of origin/destinations.
    returns nested dictionaries in a list wrapped in a dictionary, each dictionary is one set of 
    origin-destinations distance information"""

    list_distances = []
    for tup in location_dict.items():
        origin = tup[0]
        dests = tup[1]
        result = gmaps.distance_matrix(origin, dests, units="imperial")
        list_distances.append(result)

    print list_distances
    return list_distances
    #returns raw API results: nested dictionary in a nested list of dictionaries
      

def parse_results_distance(list_distances):
    """parse API results to pull list of distances only"""


    distance_list = []
    for di in list_distances:
        new_di = di['rows'][0]['elements']
        for di in new_di:
            distance = di['distance']['text']
            if ',' in distance:
                distance = distance.replace(',', '')
            distance_list.append(distance)
    distance_list = [str(i) for i in distance_list]
    distance_list = [i.rstrip(' mi') for i in distance_list]
    distance_list = [float(i) for i in distance_list]

    print distance_list
    return distance_list
    #returns [1, 2, 3, 4...20]

def parse_results_origin(list_distances):
    """parse API results to pull list of origins"""

    origin_list = []
    for o in list_distances:
        origin = o['origin_addresses']
        origin_list.append(origin)
    origin_list = [str(o[0]) for o in origin_list]

    print origin_list
    return origin_list
    #['San Francisco, CA, USA', 'San Jose, CA, USA', 'Los Angeles, CA, USA']

def parse_results_dests(list_distances):
    """parse API results to pull nested list of dests"""

    dests_list = []
    for d in list_distances:
        dest = d['destination_addresses']
        dests_list.append(dest)
    dests_list = [[str(i) for i in d] for d in dests_list]

    print dests_list
    return dests_list
    #returns [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h']]


def concat_dest_dist(distance_list, dests_list):
    """concat two lists together in order to sort in next function
    1. Match up dests_list and distance_list: 
        - create same number of sublists as dests_list
        - add each element into a new list, but new list length should be the 
        same as dests_list"""

    i = 0
    chunk = len(dests_list[0])
    ordered_dist = []
    while i < len(distance_list):
        ordered_dist.append(distance_list[i: i+chunk])
        i += chunk
    dest_dist_list = []
    for j in range(len(dests_list)):
        dest_dist_list.append(zip(dests_list[j], ordered_dist[j]))

    print dest_dist_list
    return dest_dist_list
    # returns [[('San Francisco, CA, USA', 5), ('Oakland, CA, USA', 40.7)],
    # [('San Francisco, CA, USA', 12.4), ('Fremont, CA, USA', 30)]]


def sort_distance(dest_dist_list):
    """given a list of (dest, distance)list of tuples, sort by miles so 
    tuple with smallest mileage appears first"""

    sorted_dest_dist_list = []
    for tup_list in dest_dist_list:
        s = sorted(tup_list, key=lambda y: y[1])
        sorted_dest_dist_list.append(s)
    
    print sorted_dest_dist_list
    return sorted_dest_dist_list
    # [[('Oakland, CA, USA', 40.7),('San Francisco, CA, USA', 48.5)]


def concat_origin_dest_dist(origin_list, sorted_dest_dist_list):
    """create a dictionary with origin as key, list of dest/mi tuples as value"""

    raw_list = zip(origin_list, sorted_dest_dist_list)
    origin_dest_dist_dict = dict(raw_list)
    

    print origin_dest_dist_dict
    return origin_dest_dist_dict
    #{'SF': [(city, mi), (city, mi), (city, mi)], 'Origin': [(city, mi)]}


def order_waypts(locations, origin_dest_dist_dict):
    """create a list of ordered stops, initially add only locations[0]
    which is the first element in the original user-input list, because that's 
    always going to be the start point. Then iterate through origin_dest_dist_dict
    to grab the remaining stops"""

    stops = [locations[0]]
    print stops

    i = 0
    while len(stops) < len(origin_dest_dist_dict):
        dests = origin_dest_dist_dict[stops[i]]
        next_stop = dests[0][0]
        if next_stop not in stops:
            stops.append(next_stop)
        else:
            stops.append(dests[1][0])
        i += 1

    print stops
    return stops
    #['San Francisco', 'Oakland', 'San Mateo']

def get_json(stops):
    """jsonify stops"""

    stops_d = {}
    
    stops_d[stops[0]] = stops[1:]


    print stops_d
    return jsonify(stops_d=stops_d)
    #returns {"a": 1, "b": 2, "c": 3}
    

   
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
