
import os
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
import googlemaps
from googlemaps import convert
import json
from parse_dist import *

google_api_key = os.environ["GOOGLE_MAPS_SERVER_API_KEY"]  
gmaps = googlemaps.Client(key=google_api_key)
mykey = os.environ["GOOGLE_MAPS_BROWSER_API_KEY"]


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"


@app.route("/", methods=['GET'])
def render_homepage():
    """display homepage"""

    return render_template("homepage.html",
                            mykey=mykey)


@app.route('/distance.json', methods=['POST'])
def get_list_locations():
    """get value from user input form, filter out any empty input"""

    # locations = request.form.get('loc')
    locations = request.args.getlist("loc")
    locations = filter(None, locations)

    """how to call view function in helper function? Locations is returning blank"""
    location_dict = get_api_distances(locations)
    list_distances = get_distance(location_dict)
    distance_list = parse_results_distance(list_distances)
    origin_list = parse_results_origin(list_distances)
    dests_list = parse_results_dests(list_distances)
    dest_dist_list = concat_dest_dist(distance_list, dests_list)
    sorted_dest_dist_list = sort_distance(dest_dist_list)
    origin_dest_dist_dict = concat_origin_dest_dist(origin_list, sorted_dest_dist_list)
    stops = order_stops(origin_list, origin_dest_dist_dict)

    stops_d = {}
    stops_d[stops[0]] = stops[1:]

    return jsonify(stops_d=stops_d)


# @app.route('/stops_d.json')
# def get_stops():
#     """get ordered stops"""
    

#     location_dict = get_api_distances(locations)
#     list_distances = get_distance(location_dict)
#     distance_list = parse_results_distance(list_distances)
#     origin_list = parse_results_origin(list_distances)
#     dests_list = parse_results_dests(list_distances)
#     dest_dist_list = concat_dest_dist(distance_list, dests_list)
#     sorted_dest_dist_list = sort_distance(dest_dist_list)
#     origin_dest_dist_dict = concat_origin_dest_dist(origin_list, sorted_dest_dist_list)
#     stops = order_waypts(origin_list, origin_dest_dist_dict)

#     stops_d = {}
#     stops_d[stops[0]] = stops[1:]

#     return jsonify(stops_d=stops_d)
#     #{'origin': 0, 'stop1': 1, 'stop2': 2...}

   
@app.route('/route_map')
def render_map():
    """renders map page"""

    return render_template('/route_map.html',
                            mykey=mykey)


   
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")
