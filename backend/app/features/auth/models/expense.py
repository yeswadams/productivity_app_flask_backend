from datetime import datetime, timezone
from app.extensions.database import db

class Expense(db.model):
    __tablename__='expenses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime(timezone.utc), nullable=False)
    user_id = db.Column(db.Interger, db.ForeignKey('users.id'), nullable=False, index=True)

    def __repr__(self):
        return f'<Expense {self.title} - ${self.amount}>'