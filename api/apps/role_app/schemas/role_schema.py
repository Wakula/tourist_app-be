from marshmallow import Schema, fields, validates_schema, ValidationError, validate


class RoleSchema(Schema):
    trip_id = fields.Integer(required=True, validate=validate.Range(min=1))
    name = fields.Str(validate=validate.Length(min=3, max=20), required=True)
    color = fields.Str(validate=validate.Length(equal=7), required=True)
