from flask import current_app


class PointController:

    @staticmethod
    def create_point(data, trip):
        point = current_app.models.Point.create_point(data, trip)
        return point
