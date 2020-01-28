from database import db


trip_user_table = db.Table('trip_user',
    db.Column('trip_id', db.Integer, db.ForeignKey('trip.trip_id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user_profile.user_id'), primary_key=True)
)


class Trip(db.Model):
    __tablename__ = 'trip'
    __table_args__ = {'extend_existing': True}
    trip_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Open')
    admin_id = db.Column(db.Integer, db.ForeignKey('user_profile.user_id'), nullable=False)
    points = db.relationship('Point', cascade='all, delete, delete-orphan', lazy=True, 
                         backref=db.backref('trip', lazy=True))
    trip_uuid = db.Column(db.String(36), unique=True)
    users = db.relationship('User', secondary=trip_user_table, lazy=True,
                         backref=db.backref('trips', lazy=True))
    equipment = db.relationship('apps.equipment_app.models.equipment_model.Equipment',
                         backref=db.backref('trip'),
                         cascade='all, delete, delete-orphan',
                         single_parent=True)
    roles = db.relationship('Role', backref='trip', cascade='all, delete, delete-orphan', lazy=True)



    def delete_trip(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_trip_by_id(cls, trip_id):
        return cls.query.filter_by(trip_id=trip_id).first()

    @classmethod
    def create_trip(cls, data):
        trip = cls(**data)
        trip.users.append(trip.admin)
        db.session.add(trip)
        db.session.commit()
        return trip

    @classmethod
    def get_all_trips(cls):
        return cls.query.all()

    def update_trip(self, start_date, end_date, status):
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_trip_by_uuid(cls, trip_uuid):
        return cls.query.filter_by(trip_uuid=trip_uuid).first()

    def set_uuid(self, trip_uuid):
        self.trip_uuid = trip_uuid
        db.session.add(self)
        db.session.commit()
        return self.trip_uuid

    def join_user(self, user):
        self.users.append(user)
        db.session.add(self)
        db.session.commit()
        return user

    def delete_user(self, user):
        if user in self.users:
            user_id = user.user_id
            self.users.remove(user)
            db.session.add(self)
            db.session.commit()
            return user_id
        else:
            return None

    # tofix
    def get_fields(self, args):
        public_data = {}
        if not args:
            args = list(self.__dict__.keys())
            args.extend(['users', 'admin', 'points', 'roles'])
        for field in args:
            if field in ['users', 'admin', 'equipment']:
                try:
                    public_data[field] = [field.get_public_data() for field in getattr(self, field)]
                except:
                    public_data[field] = getattr(self, field).get_public_data()
            else:
                public_data[field] = getattr(self, field)
        try:
            public_data['equipment'] = [x for x in public_data['equipment'] if x is not None]
        except:
            pass
        public_data = {k:v for k, v in public_data.items() if v}
        return public_data

    def get_trip_details(self, user_id):
        trip_details = self.get_fields(
            ['admin', 'start_date',
            'end_date', 'name',
            'status', 'users', 'trip_id']
        )
        trip_details['participants'] = len(trip_details['users'])
        del(trip_details['users'])
        if self.admin_id == user_id:
            trip_details['admin'] = '*'
        else:
            trip_details['admin'] = trip_details['admin']['name']
        trip_details['start_date'] = str(trip_details['start_date'])
        trip_details['end_date'] = str(trip_details['end_date'])
        trip_details['id'] = self.trip_id
        return trip_details

    def __repr__(self):
        return f'<Trip {self.name}>'
