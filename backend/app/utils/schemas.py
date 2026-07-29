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




class RunExperimentSchema(Schema):
    algorithm_name = fields.String(required=True)
    dataset_source = fields.String(required=True, validate=validate.OneOf(["builtin", "uploaded"]))
    dataset_key = fields.String(required=False, allow_none=True)
    dataset_id = fields.Integer(required=False, allow_none=True)
    target_column = fields.String(required=False, allow_none=True)
    items_column = fields.String(required=False, allow_none=True)
    parameters = fields.Dict(required=False, load_default=dict)

class RunComparisonSchema(Schema):
    algorithm_names = fields.List(fields.String(), required=True, validate=validate.Length(min=2, max=6))
    dataset_source = fields.String(required=True, validate=validate.OneOf(["builtin", "uploaded"]))
    dataset_key = fields.String(required=False, allow_none=True)
    dataset_id = fields.Integer(required=False, allow_none=True)
    target_column = fields.String(required=False, allow_none=True)


# Instantiate once — reusable across requests
register_schema = RegisterSchema()
login_schema = LoginSchema()
run_experiment_schema = RunExperimentSchema()
run_comparison_schema = RunComparisonSchema()