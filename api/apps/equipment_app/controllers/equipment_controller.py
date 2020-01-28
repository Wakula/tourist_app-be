from flask import g, current_app


class EquipmentController:
    @classmethod
    def _user_has_privileges(cls, trip_id=None, role_id=None, owner_id=None):
        user = cls._get_user(g.user_id)
        trip = cls._get_trip(trip_id)
        user_has_role = role_id in (role.id for role in user.roles)
        is_item_owner = owner_id == user.user_id
        is_admin = user == trip.admin
        return user_has_role or is_item_owner or is_admin

    @staticmethod
    def _get_eq(equipment_id):
        eq = current_app.models.Equipment.get_equipment_by_id(equipment_id)
        return eq

    @staticmethod
    def _get_user(user_id):
        user = current_app.models.User.get_user_by_id(user_id)
        return user

    @staticmethod
    def _get_trip(trip_id):
        trip = current_app.models.Trip.get_trip_by_id(trip_id)
        return trip

    @classmethod
    def get_equipment_data(cls, equipment_id):
        equipment = cls._get_eq(equipment_id)
        user = cls._get_user(g.user_id)
        if equipment.trip in user.trips:
            return equipment, 201
        return 'You are not member of current trip', 402

    @classmethod
    def update_equipment(cls, equipment_id, data):
        item = cls._get_eq(equipment_id)
        if cls._user_has_privileges(item.trip_id, item.role_id, item.owner_id):
            response = current_app.models.Equipment.update_equipment(equipment_id, data)
            return response, 201
        return 'You dont have rights', 402

    @classmethod
    def delete_equipment(cls, equipment_id):
        item = cls._get_eq(equipment_id)
        if cls._user_has_privileges(item.trip_id, item.role_id, item.owner_id):
            response = current_app.models.Equipment.delete_equipment(equipment_id)
            return response, 201
        return 'You dont have rights', 402

    @classmethod
    def create_equipment(cls, data):
        if cls._user_has_privileges(data['trip_id'], data.get('role_id'), data.get('owner_id')):
            response = current_app.models.Equipment.create_equipment(data)
            return response, 201
        return 'You dont have rights', 402

    @classmethod
    def assign_equipment_to_users(cls, equipment_id, users_eq_amount):
        equipment = cls._get_eq(equipment_id)
        user = cls._get_user(g.user_id)
        target_users = [cls._get_user(u_eq['user_id']) for u_eq in users_eq_amount]
        trip = cls._get_trip(equipment.trip_id)
        user_has_role = equipment.role_id in (role.id for role in user.roles)
        is_admin = user == trip.admin

        target_users_in_trip = cls._check_if_users_in_trip(target_users, trip)

        if (user_has_role or is_admin) and target_users_in_trip:
            target_equipment_amount = cls._get_incoming_eq_amount(equipment_id, users_eq_amount)
            if equipment.quantity < target_equipment_amount:
                return 'Too many items to dispense', 409

            for user_eq_amount in users_eq_amount:
                current_app.models.EquipmentUser.assign_equipment_to_user(
                    user_eq_amount['user_id'], equipment_id, user_eq_amount['equipment_amount']
                )
            return 'Items successfully dispensed', 201
        else:
            return 'You dont have rights', 201

    @staticmethod
    def _check_if_users_in_trip(users, trip):
        for user in users:
            if not trip.trip_id in (trip.trip_id for trip in user.trips):
                return False
        return True

    @staticmethod
    def _get_incoming_eq_amount(equipment_id, each_user_eq_amount):
        existing_user_eq_amount = current_app.models.EquipmentUser.get_each_user_eq_amount(equipment_id)
        for u_eq in each_user_eq_amount:
            existing_user_eq_amount[u_eq['user_id']] = u_eq['equipment_amount']

        return sum(existing_user_eq_amount.values())
