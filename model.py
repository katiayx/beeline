from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Location(db.Model):
    """Location details"""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))


    def __repr__(self):
        return "<Location('%s', '%s'>" % (self.name, self.location_id)



class Route(db.Model):
    """Stores route distances"""

    __tablename__="routes"

    #user submits - grab the locations, distance, names - store in route
    # store location pairs -- need to save all combination pairs

    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_1 = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    location_2 = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    distance = db.Integer()

    location_1 = db.relationship("Location", backref="routes")
    location_2 = db.relationship("Location", backref="routes")


    def __repr__(self):
        return "<Searched route: %s, %s, %s>" % (self.route_id, self.location_1, self.location_2)


class User_Route(db.Model):

    __tablename__='user_routes'

    user_route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    route_id = db.Column(db.PickleType(), nullable=False)

    user = db.relationship("User", backref="user_routes")
    route = db.relationship("Route", backref="user_routes")

    def __repr__(self):
        return "<User route: %s, %s, %s>" % (self.user_route_id, self.user_id, self.route_id)


class User(db.Model):
    """User login info"""

    __tablename__='users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    password = db.Column(db.String(25))
    fname = db.Column(db.String(64))
    lname = db.Column(db.String(64))


    def is_authenticated(self):
        return True

 
    def get_id(self):
        return unicode(self.user_id)

    def __repr__(self):
        """Provide basic info on user."""

        return "<User user_id=%s username=%s fname=%s lname=%s>" % (self.user_id, self.username, self.fname, self.lname)



def init_app():
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)


def connect_to_db(app, db_uri='postgres:///distance'):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)
    db.create_all()


if __name__ == "__main__":
    from flask import Flask

    app = Flask(__name__)

    connect_to_db(app)
