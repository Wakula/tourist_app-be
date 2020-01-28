from database import db


role_user_table = db.Table('role_user',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user_profile.user_id'), primary_key=True))

class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    color = db.Column(db.String(7), nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.trip_id'), nullable=False)
    users = db.relationship('User', secondary=role_user_table, lazy=True,
        backref=db.backref('roles', lazy=True))
    equipment = db.relationship('Equipment', backref=db.backref('role'), cascade='all, delete, delete-orphan', single_parent=True)

    def __repr__(self):
        return f'<Role: {self.name}>'

    @classmethod
    def create_role(cls, data):
        role = cls(**data)
        db.session.add(role)
        db.session.commit()
        return role

    @classmethod
    def delete_role(cls, role_id):
        role = cls.query.filter_by(id=role_id).first()
        db.session.delete(role)
        db.session.commit()
        

    @classmethod
    def get_role_by_id(cls, role_id):
        return cls.query.filter_by(id=role_id).first()

    @classmethod
    def get_all_roles(cls):
        return cls.query.all()

    def toggle_role(self, user):
        if user in self.users:
            self.users.remove(user)
            result = 'Role was unassign'
        else:
            self.users.append(user)
            result = 'Role was assign'
        db.session.add(self)
        db.session.commit()
        return result
