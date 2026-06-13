from marshmallow import Schema, fields, validate, ValidationError


class RegisterSchema(Schema):
    username = fields.String(
        required=True,
        validate=validate.Length(min=3, max=80)
    )
    email = fields.Email(required=True)
    password = fields.String(
        required=True,
        validate=validate.Length(min=8, max=128),
        load_only=True  # never include in serialized output
    )


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)


# Instantiate once — reusable across requests
register_schema = RegisterSchema()
login_schema = LoginSchema()