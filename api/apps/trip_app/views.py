from helper_classes.base_view import BaseView
from flask import current_app, request, g
from .schemas.trip_schema import TripSchema, UpdateTripSchema
from marshmallow import ValidationError
from werkzeug.exceptions import Unauthorized
from helper_classes.auth_decorator import login_required


class TripView(BaseView):
    def __init__(self):
        self.trip_controller = current_app.blueprints['trip'].controllers.TripController

    @login_required
    def post(self):
        try:
            trip_data = TripSchema().load(request.json)
        except ValidationError as e:
            return self._get_response(e.messages, status_code=400)
        data, status_code = self.trip_controller.create_trip(trip_data)
        return self._get_response(data, status_code=status_code)

    @login_required
    def put(self, trip_id):
        try:
            trip_data = UpdateTripSchema().load(request.json)
        except ValidationError as e:
            return self._get_response(e.messages, status_code=400)
        response, status_code = self.trip_controller.update_trip(trip_id, **trip_data)
        return self._get_response(response, status_code=status_code)

    @login_required
    def patch(self, trip_id):
        response, status_code = self.trip_controller.refresh_trip_uuid(trip_id)
        return self._get_response(response, status_code=status_code)

    @login_required
    def get(self, trip_id):
        fields = request.args.get('fields')
        if fields:
            fields = fields.split(',')
        response, status_code = self.trip_controller.get_trip_data(trip_id, fields)
        return self._get_response(response, status_code=status_code)