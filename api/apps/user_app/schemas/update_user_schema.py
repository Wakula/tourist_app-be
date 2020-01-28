from marshmallow import Schema, fields, ValidationError, validates, validate
import re


class UpdateUserSchema(Schema):

    name = fields.Str(validate=validate.Length(min=2, max=30))
    surname = fields.Str(validate=validate.Length(min=0, max=30))
    capacity = fields.Int(validate=validate.Range(min=0))
    old_password = fields.String()
    new_password = fields.String()

    @validates('new_password')
    def _validate_new_password(self, new_password):
        """password should have at least 8 symbols which has 1 digit and letter"""
        pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
        if pattern.match(new_password) is None:
            raise ValidationError('Password should be at least 8 symbols long and have at least one digit and character')




