from .point_controller import PointController
from flask import current_app, g
from helper_classes.auth_decorator import login_required
from marshmallow import ValidationError
import uuid


class TripController:

    @staticmethod
    def _get_user(user_id):
        user = current_app.models.User.get_user_by_id(user_id)
        return user

    @staticmethod
    def _get_trip(trip_id):
        trip = current_app.models.Trip.get_trip_by_id(trip_id)
        return trip

    @classmethod
    def create_trip(cls, data):
        admin = cls._get_user(g.user_id)
        data['admin'] = admin
        points = data.pop('points', None)
        trip = current_app.models.Trip.create_trip(data)
        for point in points:
            PointController.create_point(point, trip)
        trip_uuid = current_app.blueprints['otc'].controllers\
            .OtcController.create_trip_link_uuid()
        trip.set_uuid(trip_uuid)
        return trip.trip_id, 201

    @classmethod
    def refresh_trip_uuid(cls, trip_id):
        user = cls._get_user(g.user_id)
        trip = current_app.models.Trip.get_trip_by_id(trip_id)
        if trip.admin == user:
            trip_uuid = current_app.blueprints['otc'].controllers\
                .OtcController.create_trip_link_uuid(current_uuid=trip.trip_uuid)
            trip.set_uuid(trip_uuid)
            return trip.trip_uuid, 201
        return 'You are not admin of current trip', 400

    @classmethod
    def get_trip_data(cls, trip_id, fields):
        user = cls._get_user(g.user_id)
        trip = cls._get_trip(trip_id)
        if user in trip.users:
            trip_data = trip.get_fields(fields)
            if trip_data.get('trip_uuid') and trip.admin != user:
                del trip_data['trip_uuid']
            return trip_data, 201
        return ('You are not member of given trip', 400)

    # need for OTC work
    @classmethod
    def user_to_trip(cls, trip_uuid):
        user = cls._get_user(g.user_id)
        trip = current_app.models.Trip.get_trip_by_uuid(trip_uuid=trip_uuid)
        try:
            trip.join_user(user)
            return 'User assigned to trip', 200
        except:
            return 'Couldn`t assign user to trip', 400

    @classmethod
    def update_trip(cls, trip_id, *, start_date, end_date, status):
        print(start_date)
        print(end_date)
        print(status)
        trip = cls._get_trip(trip_id)
        user = cls._get_user(g.user_id)
        if user == trip.admin:
            trip.update_trip(start_date, end_date, status)
            return 'Trip was updated', 201
        return 'You are not admin of current trip', 400
