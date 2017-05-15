from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Start(db.Model):
    """Location model."""

    __tablename__ = "start"

    start_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    

    def __repr__(self):
        return "<Start('%s', '%s'>" % (self.name, self.start_id)


class Destination(db.Model):
    """Location model."""

    __tablename__ = "destinations"

    destination_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    

    def __repr__(self):
        return "<Destination('%s', '%s'>" % (self.name, self.destination_id)


class Distance(db.Model):
    """User response table."""

    __tablename__ = "distances"

    distance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_id = db.Column(db.Integer, db.ForeignKey('start.start_id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.destination_id'), nullable=False)
    distance = db.Column(db.Integer)

    start = db.relationship("Start", backref="distances")
    destination = db.relationship("Destination", backref="distances")

    def __repr__(self):
        return "<location_id1=%s, location_id2=%s, distance=%s>" % (self.location_id1, self.location_id2,
                                                                     self.distance)


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
