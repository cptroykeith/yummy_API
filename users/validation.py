from marshmallow import Schema, fields, validate



class CreateSignupInputSchema(Schema):
    # the 'required' argument ensures the field exists
    username = fields.Str(required=True, validate=[validate.Length(min=4), validate.Regexp(r'^\S.*\S$'), validate.Regexp(r'^\w+$', error="Username must be one word")])
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=[validate.Length(min=6), validate.Regexp(r'^\w+$')])


class CreateLoginInputSchema(Schema):
    # the 'required' argument ensures the field exists
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class CreateResetPasswordEmailSendInputSchema(Schema):
    # the 'required' argument ensures the field exists
    email = fields.Email(required=True)

class ResetPasswordInputSchema(Schema):
    # the 'required' argument ensures the field exists
    password = fields.Str(required=True, validate=validate.Length(min=6))

class CreateCategoryInputSchema(Schema):
    name = fields.Str(required=True, validate=[validate.Length(min=4), validate.Regexp(r'^\S.*\S$'), validate.Regexp(r'^\w+$', error="Category must be one word")])
    description = fields.Str(required=True, validate=[validate.Length(min=4), validate.Regexp(r'^\S.*\S$')])

class CreateRecipeInputSchema(Schema):
    # the 'required' argument ensures the field exists
    type = fields.Str(required=True, validate=[validate.Length(min=4), validate.Regexp(r'^\S.*\S$'), validate.Regexp(r'^\w+$', error="Type must be one word")])
    ingredients = fields.Str(required=True, validate=[validate.Length(min=4), validate.Regexp(r'^\S.*\S$')])
    steps = fields.Str(required=True, validate=[validate.Length(min=4), validate.Regexp(r'^\S.*\S$')])
    category_id = fields.Int(required=True)
