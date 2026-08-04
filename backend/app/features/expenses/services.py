from app.extensions.database import db
from app.features.expenses.models import Expense
from datetime import datetime, timezone
from typing import Optional, Dict, Any


class ExpenseService:
    @staticmethod
    def create_expense(user_id: int, title: str, amount: float, 
                      description: Optional[str] = None, 
                      date: Optional[datetime] = None) -> Expense:
        """Creates a new expense for a user"""
        
        if date is None:
            date = datetime.now(timezone.utc)
        
        expense = Expense(
            title=title,
            amount=amount,
            description=description,
            date=date,
            user_id=user_id
        )
        
        db.session.add(expense)
        db.session.commit()
        return expense

    @staticmethod
    def get_user_expenses(user_id: int, page: int = 1, per_page: int = 10) -> Dict:
        """Gets paginated expenses for a specific user"""
        
        pagination = Expense.query.filter_by(user_id=user_id)\
            .order_by(Expense.date.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'expenses': pagination.items,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': page,
            'per_page': per_page,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }

    @staticmethod
    def get_expense_by_id(expense_id: int, user_id: int) -> Expense:
        """Gets a specific expense by ID for a user"""
        
        expense = Expense.query.filter_by(id=expense_id, user_id=user_id).first()
        
        if not expense:
            raise ValueError("Expense not found or access denied")
        
        return expense

    @staticmethod
    def update_expense(expense_id: int, user_id: int, updates: Dict[str, Any]) -> Expense:
        """Updates an existing expense for a user"""
        
        expense = ExpenseService.get_expense_by_id(expense_id, user_id)
        
        for field, value in updates.items():
            setattr(expense, field, value)
        
        db.session.commit()
        return expense

    @staticmethod
    def delete_expense(expense_id: int, user_id: int) -> None:
        """Deletes an expense for a user"""
        
        expense = ExpenseService.get_expense_by_id(expense_id, user_id)
        db.session.delete(expense)
        db.session.commit()
