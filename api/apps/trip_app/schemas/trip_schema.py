from marshmallow import Schema, fields, validates_schema, ValidationError, validate
from .point_schema import PointSchema


class TripSchema(Schema):
    name = fields.Str(validate=validate.Length(min=3, max=30), required=True)
    description = fields.Str(validate=validate.Length(max=500))
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    status = fields.String(validate=validate.Length(min=1, max=20))
    points = fields.Nested(PointSchema, many=True)

    @validates_schema
    def _validate_date(self, data, **kwargs):
        start_date = data['start_date']
        end_date = data['end_date']
        if start_date > end_date:
            raise ValidationError("Start date can not be greater than end date")


class UpdateTripSchema(Schema):
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    status = fields.String(validate=validate.Length(min=1, max=20))

    @validates_schema
    def _validate_date(self, data, **kwargs):
        start_date = data['start_date']
        end_date = data['end_date']
        if start_date > end_date:
            raise ValidationError("Start date can not be greater than end date")

    @validates_schema
    def _validate_status(self, data, **kwargs):
        status = data['status']
        available_statuses = {'Open', 'Closed'}
        if status not in available_statuses:
            raise ValidationError("Status does not exist")
