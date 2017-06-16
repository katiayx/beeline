from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Location(db.Model):
    """Location details"""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'), unique=True)


    addresses = db.relationship('Address', backref='locations')


    def __repr__(self):
        return "<Location('%s', '%s', '%s'>" % (self.name, self.location_id, self.address_id)


class Address(db.Model):
    """Child table of Location: contains address components"""

    __tablename__ = "addresses"

    address_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    number = db.Column(db.Integer)
    street = db.Column(db.String(250))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(15))
    zipcode = db.Column(db.Integer)
    country = db.Column(db.String(100))


    def __repr__(self):
        return "<Address('%s', '%s', '%s', '%s', '%s'>" % (self.number, self.street, self.city, self.state, self.zipcode)


class Distance(db.Model):
    """Stores distance data for two locations"""

    __tablename__ = "distances"

    distance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    location_1_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    location_2_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    distance = db.Column(db.Integer)

    location_1 = db.relationship('Location', backref='distances')
    location_2 = db.relationship('Location', backref='distances')


    def __repr__(self):
        return "<location_id1=%s, location_id2=%s, distance=%s>" % (self.location_1_id, self.location_2_id, self.distance)


class Route(db.Model):
    """Stores routes searched by user"""

    __tablename__="routes"

    route_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    location_1_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    location_2_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'), nullable=False)
    location_3_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    location_4_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))
    location_5_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))

    user = db.relationship("User", backref="routes")
    location_1 = db.relationship("Location", backref="routes")
    location_2 = db.relationship("Location", backref="routes")
    location_3 = db.relationship("Location", backref="routes")
    location_4 = db.relationship("Location", backref="routes")
    location_5 = db.relationship("Location", backref="routes")


    def __repr__(self):
        return "<Searched route: %s, %s, %s, %s, %s>" % (self.location_1_id, self.location_2_id, self.location_3_id,
                                                                     self.location_4_id, self.location_5_id)


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
