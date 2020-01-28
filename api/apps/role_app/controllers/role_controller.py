from flask import current_app, g


class RoleController:

    @staticmethod
    def _get_trip(trip_id):
        trip = current_app.models.Trip.get_trip_by_id(trip_id)
        return trip

    @staticmethod
    def _get_user(user_id):
        user = current_app.models.User.get_user_by_id(user_id)
        return user
    
    @staticmethod
    def _get_role(role_id):
        role = current_app.models.Role.get_role_by_id(role_id)
        return role

    @classmethod
    def get_role(cls, role_id):
        user = cls._get_user(g.user_id)
        role = current_app.models.Role.get_role_by_id(role_id)
        if role.trip_id in map(lambda x: x.trip_id, user.trips):
            return role, 201
        return 'You have no rights', 401

    @classmethod
    def create_role(cls, data):
        user = cls._get_user(g.user_id)
        trip = cls._get_trip(data['trip_id'])
        if user == trip.admin:
            return current_app.models.Role.create_role(data), 201
        else:
            return 'You are not admin of current trip', 401

    @classmethod
    def toggle_role(cls, role_id, user_id):
        role = cls._get_role(role_id)
        user = cls._get_user(user_id)
        admin = cls._get_user(g.user_id)
        trip = cls._get_trip(role.trip_id)
        if trip.admin == admin and user in trip.users:
            return role.toggle_role(user), 201
        else:
            return 'Assigning role failed', 401

    @classmethod
    def delete_role(cls, role_id):
        user = cls._get_user(g.user_id)
        role = cls._get_role(role_id)
        if role.trip_id in map(lambda x: x.trip_id, user.admin_trips):
            current_app.models.Role.delete_role(role_id)
            return f"Role {role_id} successfully deleted", 201
        return 'You are not admin of current trip', 401
