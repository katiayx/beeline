
import os
from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined
import json

mykey = os.environ.get("GOOGLE_MAPS_BROWSER_API_KEY")

# mykey = os.environ["GOOGLE_MAPS_BROWSER_API_KEY"]

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

from parse_dist import(get_lists, get_api_distance, parse_results_distance, parse_results_origin, parse_results_dests,
concat_dest_dist, sort_distance, concat_origin_dest_dist, get_origin_stop, order_stops)



@app.route('/')
def render_homepage():
    """display homepage"""

    return render_template('homepage.html',
                            mykey=mykey)


@app.route('/route_map', methods=['POST'])
def get_list_locations():
    """get value from user input form, filter out any empty input
    call helper functions to call distance API, parse returned results
    compare distance and return list of stops"""

    locations = request.form.getlist("loc")
    locations = filter(None, locations)

    location_dict = get_lists(locations)
    list_distances = get_api_distance(location_dict)
    distance_list = parse_results_distance(list_distances)
    origin_list = parse_results_origin(list_distances)
    dests_list = parse_results_dests(list_distances)
    dest_dist_list = concat_dest_dist(distance_list, dests_list)
    sorted_dest_dist_list = sort_distance(dest_dist_list)
    origin_dest_dist_dict = concat_origin_dest_dist(origin_list, sorted_dest_dist_list)
    start = get_origin_stop(locations)
    stops = order_stops(start, origin_dest_dist_dict)

    origin = stops[0]
    destination = stops[-1]
    waypts = stops[1: -1]

    return render_template('/route_map.html',
                            origin=origin,
                            destination=destination,
                            waypts=waypts,
                            mykey=mykey)
    # stops = ['San Francisco, CA, USA', 'Oakland, CA, USA', 'Orinda, CA, USA', 'San Mateo, CA, USA', 'Mountain View, CA, USA']
    # origin = San Francisco, CA, USA
    # destination = Mountain View, CA, USA
    # waypts = ['Oakland, CA, USA', 'Orinda, CA, USA', 'San Mateo, CA, USA']


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    # app.debug = True

    # Use the DebugToolbar
    # DebugToolbarExtension(app)
    
    # app.run(host="0.0.0.0")

    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
