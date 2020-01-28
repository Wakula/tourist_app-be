from marshmallow import Schema, fields, validates_schema, ValidationError, validate


class PointSchema(Schema):
    order_number = fields.Integer(required=True, validate=validate.Range(min=1))
    name = fields.Str(validate=validate.Length(min=3, max=30), required=True)
    latitude = fields.Float(required=True, validate=validate.Range(min=-90, max=90))
    longitude = fields.Float(required=True, validate=validate.Range(min=-180, max=180))
