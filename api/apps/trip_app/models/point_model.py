from database import db


class Point(db.Model):
    __tablename__ = 'point'
    __table_args__ = {'extend_existing': True}
    point_id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.trip_id'), nullable=False)

    @classmethod
    def create_point(cls, data, trip):
        point = cls(**data, trip=trip)
        db.session.add(point)
        db.session.commit()
        return point

    def __repr__(self):
        return f'<Point lat: {self.latitude} long: {self.longitude}>'

