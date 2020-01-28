from database import db


class EquipmentUser(db.Model):
    __tablename__ = 'equipment_user'
    __table_args__ = {'extend_existing': True}

    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.equipment_id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_profile.user_id'), primary_key=True)
    amount = db.Column(db.Integer, nullable=False)

    @classmethod
    def get_existing_user_equipment(cls, user_id, equipment_id):
        res = cls.query.filter_by(equipment_id=equipment_id, user_id=user_id).first()
        return res

    @classmethod
    def assign_equipment_to_user(cls, user_id, equipment_id, amount):
        existing_user_equipment = cls.get_existing_user_equipment(user_id, equipment_id)
        if existing_user_equipment:
            existing_user_equipment.amount = amount
            db.session.commit()
            return

        equipment_user = cls(equipment_id=equipment_id, user_id=user_id, amount=amount)
        db.session.add(equipment_user)
        db.session.commit()

    @classmethod
    def get_each_user_eq_amount(cls, equipment_id):
        return {
            eq_u.user_id: eq_u.amount for eq_u in  cls.query.filter_by(equipment_id=equipment_id).all()
        }


class Equipment(db.Model):
    """Model for equipment"""

    __tablename__ = 'equipment'
    __table_args__ = {'extend_existing': True}

    equipment_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trip.trip_id'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user_profile.user_id'),
        nullable=True)
    owner = db.relationship('User', backref='personal_stuff')
    users = db.relationship('User', secondary='equipment_user', lazy='dynamic',
                            backref=db.backref('equipment', lazy='dynamic'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=True)

    @classmethod
    def create_equipment(cls, data):
        """Create new equipment in the item list"""

        equipment = cls(**data)
        db.session.add(equipment)
        db.session.commit()
        return equipment

    @classmethod
    def get_equipment_by_id(cls, id):
        """Return the equipment by id"""

        return cls.query.filter_by(equipment_id=id).first()

    @classmethod
    def update_equipment(cls, id, updated_data):
        """Update equipment data in the list of items"""

        equipment = cls.get_equipment_by_id(id)
        equipment.role_id = updated_data.get('role_id')
        equipment.name = updated_data['name']
        equipment.weight = updated_data['weight']
        equipment.quantity = updated_data['quantity']
        db.session.commit()
        return equipment

    @classmethod
    def delete_equipment(cls, id):
        """Delete equipment from the list of items"""

        equipment = cls.get_equipment_by_id(id)
        db.session.delete(equipment)
        db.session.commit()
        return 'Successfully deleted'

    def get_public_data(self):
        if not self.owner_id:
            users = []
            for user in self.users:
                equipment_user = EquipmentUser.get_existing_user_equipment(
                    user.user_id, self.equipment_id
                )
                if equipment_user.amount > 0:
                    users.append({
                        'user_id': equipment_user.user_id,
                        'amount': equipment_user.amount
                    })
            res = dict(self.__dict__)
            res['users'] = users
            return res

    def get_quantity(self, user_id):
        equipment_user = EquipmentUser.get_existing_user_equipment(user_id, self.equipment_id)
        self.quantity = equipment_user.amount
        return self

    def __repr__(self):
        return f'Equipment: {self.name}'
