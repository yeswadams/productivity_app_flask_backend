from marshmallow import fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.extensions.database import db
from app.features.expenses.models import Expense

class ExpenseSchema(SQLAlchemyAutoSchema):
    """Used to validate the incoming data from POST/PATCH Request"""
    class Meta:
        model = Expense
        sqla_session = db.session
        load_instance = False
        include_fk = True

    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1, max=120))
    amount = fields.Float(required=True, validate=validate.Range(min=0.01))
    description = fields.String(allow_none=True)
    date = fields.DateTime(allow_none=True)
    user_id = fields.Integer(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

# Singleton instance for clean imports
expense_schema = ExpenseSchema()