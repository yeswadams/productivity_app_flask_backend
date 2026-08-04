from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.features.expenses.schemas.expense_schema import expense_schema
from app.features.expenses.services import ExpenseService

expenses_bp = Blueprint(
    'expenses', 
    __name__
)


@expenses_bp.route('', methods=['GET'])
@jwt_required()
def get_expenses():
    """GET /api/v1/expenses - Get paginated expenses for current user"""
    
    try:
        current_user_id = int(get_jwt_identity())
        
        # Get pagination parameters from query string
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Validate pagination parameters
        if page < 1:
            return jsonify({"message": "Page must be greater than 0"}), 400
        if per_page < 1 or per_page > 100:
            return jsonify({"message": "Per page must be between 1 and 100"}), 400
        
        result = ExpenseService.get_user_expenses(current_user_id, page, per_page)
        
        return jsonify({
            "expenses": expense_schema.dump(result['expenses'], many=True),
            "pagination": {
                "total": result['total'],
                "pages": result['pages'],
                "current_page": result['current_page'],
                "per_page": result['per_page'],
                "has_next": result['has_next'],
                "has_prev": result['has_prev']
            }
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Error retrieving expenses: {str(e)}"}), 500


@expenses_bp.route('', methods=['POST'])
@jwt_required()
def create_expense():
    """POST /api/v1/expenses - Create a new expense for current user"""
    
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    
    try:
        data = expense_schema.load(json_data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422
    
    try:
        current_user_id = int(get_jwt_identity())
        
        expense = ExpenseService.create_expense(
            user_id=current_user_id,
            title=data['title'],
            amount=float(data['amount']),
            description=data.get('description'),
            date=data.get('date')
        )
        
        return jsonify({
            "message": "Expense created successfully",
            "expense": expense_schema.dump(expense)
        }), 201
        
    except ValueError as err:
        return jsonify({"message": str(err)}), 400
    except Exception as e:
        return jsonify({"message": f"Error creating expense: {str(e)}"}), 500


@expenses_bp.route('/<int:expense_id>', methods=['GET'])
@jwt_required()
def get_expense(expense_id):
    """GET /api/v1/expenses/<id> - Get a specific expense by ID"""
    
    try:
        current_user_id = int(get_jwt_identity())
        
        expense = ExpenseService.get_expense_by_id(expense_id, current_user_id)
        
        return jsonify({
            "expense": expense_schema.dump(expense)
        }), 200
        
    except ValueError as err:
        return jsonify({"message": str(err)}), 404
    except Exception as e:
        return jsonify({"message": f"Error retrieving expense: {str(e)}"}), 500


@expenses_bp.route('/<int:expense_id>', methods=['PATCH'])
@jwt_required()
def update_expense(expense_id):
    """PATCH /api/v1/expenses/<id> - Update an existing expense"""
    
    json_data = request.get_json()
    if not json_data:
        return jsonify({"message": "No input data provided"}), 400
    
    try:
        # Use partial=True to allow partial updates
        data = expense_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422
    
    try:
        current_user_id = int(get_jwt_identity())
        
        expense = ExpenseService.update_expense(
            expense_id=expense_id,
            user_id=current_user_id,
            updates={field: data[field] for field in ('title', 'amount', 'description', 'date') if field in data}
        )
        
        return jsonify({
            "message": "Expense updated successfully",
            "expense": expense_schema.dump(expense)
        }), 200
        
    except ValueError as err:
        return jsonify({"message": str(err)}), 404
    except Exception as e:
        return jsonify({"message": f"Error updating expense: {str(e)}"}), 500


@expenses_bp.route('/<int:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    """DELETE /api/v1/expenses/<id> - Delete an expense"""
    
    try:
        current_user_id = int(get_jwt_identity())
        
        ExpenseService.delete_expense(expense_id, current_user_id)
        
        return jsonify({
            "message": "Expense deleted successfully"
        }), 200
        
    except ValueError as err:
        return jsonify({"message": str(err)}), 404
    except Exception as e:
        return jsonify({"message": f"Error deleting expense: {str(e)}"}), 500
