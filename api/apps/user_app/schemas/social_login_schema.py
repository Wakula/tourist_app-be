from marshmallow import Schema, fields, validate, validates, ValidationError


class SocialLoginSchema(Schema):
    auth_token = fields.String(required=True, validate=validate.Length(min=1, max=250))
    provider = fields.String(required=True, validate=validate.Length(min=6, max=8))

    @validates('provider')
    def _validate_provider(self, provider):
        if not provider in ('FACEBOOK', 'GOOGLE'):
            raise ValidationError('Incorrect provider')
