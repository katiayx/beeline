
import os

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from werkzeug.contrib.profiler import ProfilerMiddleware

from model import connect_to_db, db, Location, Route, User_Route, User

# from flask.ext.bcrypt import Bcrypt
# from flask.ext.login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user, login_required

# from wtforms import StringField, PasswordField
# from wtforms.fields.html5 import EmailField
# from wtforms.validators import DataRequired, Email

mykey = os.environ.get("GOOGLE_MAPS_BROWSER_API_KEY")

app = Flask(__name__)
# bcrypt = Bcrypt(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# from parse_dist import(create_api_request, call_distance_api, parse_results_distance, parse_results_origin, parse_results_dests,
# concat_dest_dist, sort_distance, concat_origin_dest_dist, get_origin_stop, order_stops)



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

    
    search_database()

    return "Locations added"

    # api_request = create_api_request(user_input)
    # list_distances = call_distance_api(api_request)
    # distance_list = parse_results_distance(list_distances)
    # origin_list = parse_results_origin(list_distances)
    # dests_list = parse_results_dests(list_distances)
    # dest_dist_list = concat_dest_dist(distance_list, dests_list)
    # sorted_dest_dist_list = sort_distance(dest_dist_list)
    # origin_dest_dist_dict = concat_origin_dest_dist(origin_list, sorted_dest_dist_list)
    # start = get_origin_stop(user_input)
    # stops = order_stops(start, origin_dest_dist_dict)

    # origin = stops[0]
    # destination = stops[-1]
    # waypts = stops[1: -1]

    # return render_template('/route_map.html',
    #                         origin=origin,
    #                         destination=destination,
    #                         waypts=waypts,
    #                         mykey=mykey)
    # stops = ['San Francisco, CA, USA', 'Oakland, CA, USA', 'Orinda, CA, USA', 'San Mateo, CA, USA', 'Mountain View, CA, USA']
    # origin = San Francisco, CA, USA
    # destination = Mountain View, CA, USA
    # waypts = ['Oakland, CA, USA', 'Orinda, CA, USA', 'San Mateo, CA, USA']


def search_database():
    """Check if distance information already exists in db for inputed locations """

    user_input = request.form.getlist("loc")
    user_input = filter(None, user_input)
    #[San Francisco, CA USA, Oakland, CA USA, San Leandro, CA USA]

    input_pairs = []
    for i in xrange(len(user_input) - 1):
        for j in xrange(i + 1, len(user_input)):
            input_pairs.append([user_input[i], user_input[j]])

    print "input_pairs ", input_pairs
    #[(San Francisco, CA USA, Oakland, CA USA), (Oakland, CA USA, San Leandro, CA USA)]

    #look up each pair in db
    for locations in input_pairs:
        location_1 = locations[0]
        location_2 = locations[1]
        route = Route.query.filter(location_1==location_1 and location_2==location_2) #need to add OR to check loc_1 = loc_2, etc.
        if not route:
            route = Route(location_1==location_1,location_2==location_2)
            db.session.add(route)
            db.session.commit()



if __name__ == "__main__":
    app.config['PROFILE'] = True
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[50])
    

    # DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=True)
