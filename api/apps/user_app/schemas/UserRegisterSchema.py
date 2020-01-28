from marshmallow import Schema, fields, ValidationError, validates, validate
import re


class UserRegisterSchema(Schema):

    name = fields.Str(required=True, validate=validate.Length(min=2, max=30))
    surname = fields.Str(validate=validate.Length(min=2, max=30))
    email = fields.Email(required=True, error_messages={"required": "Email is required."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."})

    @validates("password")
    def validate_password_length(self, password):
        """password should have at least 8 symbols which has 1 digit and letter"""
        pattern = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$")
        if pattern.match(password) is None:
            raise ValidationError("Password should be at least 8 symbols long and have at least one digit and character")




