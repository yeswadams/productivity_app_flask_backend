from app.extensions.database import db
from datetime import datetime, timezone

class Expense(db.model):
    __tablename__ = 'expenses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)

    amount = db.Column(db.Numeric(10, 2), nullable=False)

    description = db.Column(db.Text, nullable=True)
    date= db.Column(db.DateTime, default=datetime(timezone.utc))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Check constraints
    __table_args__ = (
        db.CheckConstraint('amount > 0', name='ck_expenses_amount_positive'),
        db.CheckConstraint("length(title) >=1", name='ck_expenses_title_not_empty')
    ) 

    def __repr__(self):
        return f"<Expense {self.title} - ${self.amount}"