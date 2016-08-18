
import os

# from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension
from datetime import datetime

import googlemaps
from googlemaps import convert

from geopy import geocoders

google_api_key = os.environ["GOOGLE_MAPS_SERVER_API_KEY"]
    
gmaps = googlemaps.Client(key=google_api_key)


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route("/")
def index():
    """display homepage"""

    mykey = os.environ["GOOGLE_MAPS_BROWSER_API_KEY"]

    return render_template("homepage.html",
                            mykey=mykey)



# @app.route("/distance") 
# def get_latlong():
#     """ccc"""

    
#     locations = request.args.getlist("loc")  
#     addresses = filter(None, locations)
#     for point in addresses:
#         point = geolocator.geocode(point)
#         x = point.latitude
#         y = point.longitude


#     print (address.latitude, address.longitude)


#     return redirect('/')


@app.route('/distance')
def get_list_locations():
    """get value from user input form, filter out any empty input"""

    locations = request.args.getlist("loc")  
    locations = filter(None, locations)
    #returns a list: ['san francisco', 'san jose', 'oakland']

def get_distance():
    locations = get_list_locations()
    origin = locations[0]
    dests = locations[1:]
    distance = gmaps.distance_matrix(origin, dests, units="imperial")

    dist = [distance['rows'][0]['elements'][x]['distance']['text'] for x in [0,1]]
    city = [distance['destination_addresses'][x] for x in [0,1]]
    city_distance = zip(city, dist)
    dict(city_distance)
    print dict(city_distance)
    #returns a dictionary of key value pairs {'san jose': 123}

def get_first_stop():
    """compare orign and destination distance among four pair of values"""

    stops = get_first_stop() #call distance function to get dictionary
    stop_1 = min(stops, key=stops.get) #sort dictionary to find minimum
    stop_1 = str(stop_1)
    return stop_1
    #returns string 'Oakland, CA, USA'

def get_next_distance():
    """"""

    x = get_list_locations() #get original list
    x = x.pop(0) #removes origin, returns the rest of the list
    origin = get_first_stop() #calls compare distance to get new origin
    dests = [] 
    for i in get_list_locations:
        if i == origin:
            pass
        else:
            dests.append[i]
    return origin, dests

    distance = gmaps.distance_matrix(origin, dests, units="imperial")










## Calls Distance APi to grab all distance calculation by step through the list
# @app.route("/distance") 
# def get_loclists():
#     """import user input locations and create 4 lists, one with each previous 
#     location removed. To be used in distance matrix API call"""

#     google_api_key = os.environ["GOOGLE_MAPS_SERVER_API_KEY"]
    
#     gmaps = googlemaps.Client(key=google_api_key)
#     # origin = request.args.get("startpt")
#     # dests = request.args.getlist("loc")
#     locations = request.args.getlist("loc")  #list of origin plus 4 locations
#     locations = filter(None, locations)

#     # print locations
#     # for i in range(len(locations)-1):
#     #     origin = locations[i]
#     #     dests = locations[i+1:]
#         # distance = gmaps.distance_matrix(origin, dests, units="imperial")
#     #     print distance

#     return redirect('/')
    
    # ## did not need: while loop to create multiple lists
    # i = 0
    # dests = []
    #     while i <= len(locations)-2: #stepping through 
    #         origin = locations[i]
    #         destinations = locations[i+1:]
    #         dests.append([origin, destinations])
    #         i += 1
    # # print locations


# def org_dest_dist():
#     """Unpack JSON results to grab only destination, distance information
#     and then further unpack to grab """ 

#     distance_matrix = get_loclists()

#     for i in distance_matrix:
#         distance = [d['rows'][0]['elements'][i]['distance']['text']
#         i -= 1

    # dis = [d['rows'][0]['elements'][x]['distance']['text'] for x in [0, 1, 2, 3,]]
    # #can I do x < 4?
    # dest = [d['destination_addresses'][x] for x in [0,1,2,3]]
    # distance = zip(dis, dest)
    # #returns [(u'Oakland, CA, USA', u'12.3 mi'), ...]
    # for i in distance:
    #     miles = i[1]
    #     miles = miles.rstrip('mi')
    #     float(miles)
    #returns 12.3




# def find_distance():
#     """tbd"""

#     location_list = get_loclists()
#     print location_list
#     for l in location_list:
#         origin = l[0]
#         dests = l[1]
#         distance = gmaps.distance_matrix(origin, dests, units="imperial")
#             print distance

# find_distance()



    
# def reset_startpt():
#     """reset start point"""

#     point_1 = compare_distance()
#     point_dist = del point_dist[point_1]


@app.route("/route_map")
def render_map_view():
    """securely pass map_browser_api key to render google map"""

    mykey = os.environ["GOOGLE_MAPS_BROWSER_API_KEY"]

    print map_browser_api

    return render_template("route_map.html",
                            mykey=mykey)




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
