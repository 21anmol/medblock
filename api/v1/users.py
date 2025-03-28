"""
User API Routes for MedBlock

This module defines the API endpoints for user management.
"""

import os
import sys
import json
import logging
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
import jwt

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.models import Session
from utils.database import create_user, get_user_by_id, get_user_by_username
from utils.helpers import hash_password, verify_password, is_valid_email, is_valid_password
from config.config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES

# Set up logger
logger = logging.getLogger(__name__)

# Initialize blueprint
users_blueprint = Blueprint('users', __name__, url_prefix='/api/v1/users')

# Helper function to generate JWT token
def generate_token(user_id, user_role):
    """Generate a JWT token for a user"""
    payload = {
        'user_id': user_id,
        'role': user_role,
        'exp': datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TOKEN_EXPIRES),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

# User authentication required decorator
def auth_required(f):
    """Decorator to require authentication for an endpoint"""
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Authentication required'}), 401
        
        try:
            # Extract token
            token = auth_header.split(' ')[1]
            
            # Decode token
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            
            # Add user_id to request
            request.user_id = payload['user_id']
            request.user_role = payload['role']
            
            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return jsonify({'error': 'Authentication failed'}), 401
    
    decorated.__name__ = f.__name__
    return decorated

# Define API endpoints
@users_blueprint.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate email
        if not is_valid_email(data['email']):
            return jsonify({'error': 'Invalid email address'}), 400
        
        # Validate password strength
        if not is_valid_password(data['password']):
            return jsonify({'error': 'Password must be at least 8 characters and contain uppercase, lowercase, digit, and special character'}), 400
        
        # Check if username or email already exists
        session = Session()
        try:
            existing_user = session.query(User).filter(
                (User.username == data['username']) | (User.email == data['email'])
            ).first()
            
            if existing_user:
                if existing_user.username == data['username']:
                    return jsonify({'error': 'Username already taken'}), 400
                else:
                    return jsonify({'error': 'Email already registered'}), 400
                    
        finally:
            session.close()
        
        # Hash password
        password_hash = hash_password(data['password'])
        
        # Prepare user data
        user_data = {
            'username': data['username'],
            'email': data['email'],
            'password_hash': password_hash,
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'role': data['role']
        }
        
        # Add optional fields
        optional_fields = ['blockchain_address', 'date_of_birth', 'gender', 'blood_type', 
                           'height', 'weight', 'phone_number', 'address', 'city', 
                           'state', 'country', 'zip_code']
        
        for field in optional_fields:
            if field in data:
                user_data[field] = data[field]
        
        # Create user
        user = create_user(**user_data)
        
        # Generate token
        token = generate_token(user.id, user.role)
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': user.id,
            'token': token
        }), 201
        
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        return jsonify({'error': str(e)}), 500

@users_blueprint.route('/login', methods=['POST'])
def login():
    """Login a user"""
    try:
        data = request.json
        
        # Validate required fields
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Get user by username
        user = get_user_by_username(data['username'])
        
        # Check if user exists and verify password
        if not user or not verify_password(user.password_hash, data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Check if user is active
        if not user.is_active:
            return jsonify({'error': 'Account is inactive'}), 403
        
        # Update last login time
        session = Session()
        try:
            user.last_login = datetime.utcnow()
            session.commit()
        finally:
            session.close()
        
        # Generate token
        token = generate_token(user.id, user.role)
        
        return jsonify({
            'message': 'Login successful',
            'user_id': user.id,
            'token': token,
            'role': user.role,
            'name': user.full_name
        })
        
    except Exception as e:
        logger.error(f"Error logging in: {str(e)}")
        return jsonify({'error': str(e)}), 500

@users_blueprint.route('/profile', methods=['GET'])
@auth_required
def get_profile():
    """Get user profile"""
    try:
        # Get user from database
        user = get_user_by_id(request.user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Prepare profile data
        profile = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.full_name,
            'role': user.role,
            'blockchain_address': user.blockchain_address,
            'is_verified': user.is_verified,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None
        }
        
        # Add patient-specific fields if available
        if user.role == 'patient':
            profile.update({
                'date_of_birth': user.date_of_birth.isoformat() if user.date_of_birth else None,
                'age': user.age,
                'gender': user.gender,
                'blood_type': user.blood_type,
                'height': user.height,
                'weight': user.weight,
                'bmi': user.bmi
            })
        
        # Add contact information
        profile.update({
            'phone_number': user.phone_number,
            'address': user.address,
            'city': user.city,
            'state': user.state,
            'country': user.country,
            'zip_code': user.zip_code
        })
        
        return jsonify(profile)
        
    except Exception as e:
        logger.error(f"Error getting profile: {str(e)}")
        return jsonify({'error': str(e)}), 500

@users_blueprint.route('/profile', methods=['PUT'])
@auth_required
def update_profile():
    """Update user profile"""
    try:
        data = request.json
        
        # Get user from database
        session = Session()
        try:
            user = session.query(User).filter(User.id == request.user_id).first()
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            # Fields that cannot be updated
            restricted_fields = ['id', 'username', 'password_hash', 'role', 'is_active', 
                                 'is_verified', 'created_at', 'updated_at', 'last_login']
            
            # Update user fields
            updated_fields = []
            for key, value in data.items():
                if key not in restricted_fields and hasattr(user, key):
                    setattr(user, key, value)
                    updated_fields.append(key)
            
            # If height or weight is updated, recalculate BMI
            if 'height' in updated_fields or 'weight' in updated_fields:
                user.calculate_bmi()
            
            # Save changes
            session.commit()
            
            return jsonify({
                'message': 'Profile updated successfully',
                'updated_fields': updated_fields
            })
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        return jsonify({'error': str(e)}), 500

@users_blueprint.route('/all', methods=['GET'])
@auth_required
def get_all_users():
    """Get all users (admin only)"""
    try:
        # Check if user is admin
        if request.user_role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        
        # Get all users
        session = Session()
        try:
            users = session.query(User).all()
            
            # Format user data
            user_list = [{
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role,
                'is_active': user.is_active,
                'is_verified': user.is_verified,
                'created_at': user.created_at.isoformat() if user.created_at else None
            } for user in users]
            
            return jsonify(user_list)
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error getting all users: {str(e)}")
        return jsonify({'error': str(e)}), 500 