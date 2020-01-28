from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

BASE_AVATAR_LINK = 'http://localhost:5000/static/images/user_avatar.png'


class User(db.Model):
    """Model for user accounts."""

    __tablename__ = 'user_profile'
    __table_args__ = {'extend_existing': True}

    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(15), nullable=False)
    surname = db.Column(db.String(60), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=True)
    avatar = db.Column(db.String(250), nullable=True)
    capacity = db.Column(db.Integer, nullable=False, default=20)
    uuid = db.Column(db.String(36), nullable=True)
    is_active = db.Column(db.Boolean, default=False)
    registration_time = db.Column(db.DateTime, default=datetime.utcnow())
    admin_trips = db.relationship('Trip', lazy=True, 
        cascade='all, delete, delete-orphan', backref=db.backref('admin', lazy=True))

    def __repr__(self):
        return f'<User {self.name}>'

    @classmethod
    def create_user(cls, name, email, password=None, surname=None,
                    is_active=False, avatar=BASE_AVATAR_LINK):
        password_hash = generate_password_hash(password) if password else None
        user = cls(name=name, email=email, password_hash=password_hash, 
                    surname=surname, is_active=is_active, avatar=avatar)
        db.session.add(user)
        db.session.commit()
        return user

    def set_uuid(self, uuid):
        self.uuid = uuid
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def update_user(cls, data, user_id=user_id):
        cls.query.filter_by(user_id=user_id).update(data)
        db.session.commit()

    @classmethod
    def get_user_by_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def get_user_by_uuid(cls, uuid):
        return User.query.filter_by(uuid=uuid).first()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        db.session.commit()

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def password_is_set(self):
        return self.password_hash is not None

    def activate_user(self):
        self.is_active = True
        db.session.add(self)
        db.session.commit()

    def change_capacity(self, capacity):
        self.capacity = capacity
        db.session.add(self)
        db.session.commit()

    def change_public_fields(self, name, surname, capacity):
        self.capacity = capacity
        self.name = name
        self.surname = surname
        db.session.add(self)
        db.session.commit()

    def change_avatar_url(self, avatar):
        self.avatar = avatar
        db.session.add(self)
        db.session.commit()

    def is_uuid_valid(self):
        datetime_diff = datetime.utcnow() - self.registration_time
        diff_in_hours = datetime_diff.total_seconds() / 3600
        if diff_in_hours > 24:
            return False
        return True

    def get_public_data(self):
        public_data = {
            "user_id": self.user_id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "avatar": self.avatar,
            "capacity": self.capacity,
            "roles": self.roles,
            "passwordIsSet": self.password_is_set(),
        }
        return public_data

    # tofix
    def get_fields(self, fields, *, trip_id=None):
        public_data = {}
        if not fields:
            return self.get_public_data()
        for field in fields:
            if field == 'roles':
                public_data[field] = [role for role in getattr(self, field) if role.trip_id == trip_id]
            elif field == 'trips':
                public_data[field] = [trip.get_trip_details(self.user_id) for trip in getattr(self, field)]
            elif field == 'equipment':
                item_list = getattr(self, field).filter_by(trip_id=trip_id).all()
                public_data[field] = [item.get_quantity(self.user_id) for item in item_list if item.get_quantity(self.user_id).quantity > 0]
            elif field == 'personal_stuff':
                public_data[field] = [item for item in getattr(self, field) if item.trip_id == trip_id]
            else:
                public_data[field] = getattr(self, field)
        return public_data
