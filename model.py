"""Models and database functions for HB project."""
import heapq
import time
from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# setting up user table

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_name=%s>" % (self.user_name)

##############################################################################
# setting up Route class: each route is made up of 1 origin and many stops (number of)

class Route(db.Model):
    """TBD"""

    __tablename__ = "routes"

    route_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), 
        nullable=False)
    origin = db.Column(db.String(100))
    num_stops = db.Column(db.Integer)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Route route_id=%s origin=%s num_stops=%d>" % (self.route_id, 
            self.origin, self.num_stops)

    # Define relationship to user
    user = db.relationship("User",
                           backref=db.backref("users", order_by=user_id))

##############################################################################
# setting up Stop class: each stop is an address

class Stop(db.Model):
    """TBD"""

    __tablename__ = "stops"

    stop_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    stop = db.Column(db.String(100))


##############################################################################
# setting up Position class: each stop has a unique position within each route 
# middle table linking Route class and Stop class

class Position(db.Model):
    """TBD"""

    __tablename__ = "positions"

    position_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    route_id = db.Column(db.interger, db.ForeignKey('routes.route_id'), nullable=False)
    stop_id = db.Column(db.interger, db.ForeignKey('stops.stop_id'), nullable=False)
    position = db.Column(db.interger)

    stop = db.relationship('Stop', backref='positions')
    route = db.relationship('Route', backref='positions')
   

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Position position_id=%d route_id=%d stop_id=%d position=%d>" % (
            self.position_id, self.route_id, self.stop_id, self.position)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///routes'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
