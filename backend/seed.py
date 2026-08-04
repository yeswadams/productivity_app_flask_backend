"""Create local development data for the Productivity App."""

from datetime import datetime, timedelta, timezone

from app import create_app
from app.extensions.database import db
from app.features.auth.models import User
from app.features.expenses.models import Expense


def seed_database():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        ada = User(username="ada")
        ada.set_password("password123")
        sam = User(username="sam")
        sam.set_password("password123")
        db.session.add_all([ada, sam])
        db.session.flush()

        now = datetime.now(timezone.utc)
        db.session.add_all([
            Expense(title="Groceries", amount=42.50, description="Weekly food shop", date=now, user_id=ada.id),
            Expense(title="Transport", amount=15.00, description="Bus fare", date=now - timedelta(days=1), user_id=ada.id),
            Expense(title="Internet", amount=30.00, description="Monthly data plan", date=now - timedelta(days=2), user_id=sam.id),
        ])
        db.session.commit()
        print("Seeded 2 users and 3 expenses.")


if __name__ == "__main__":
    seed_database()
