"""
Medical Records API Routes for MedBlock

This module defines the API endpoints for medical record management.
"""

import os
import sys
import json
import logging
from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.models import Session, MedicalRecord, User
from utils.database import create_medical_record, get_medical_records_for_patient, log_record_access
from utils.helpers import load_encryption_key, generate_unique_id
from config.config import BLOCKCHAIN_KEY_FILE

# Import authentication decorator from users module
from .users import auth_required

# Set up logger
logger = logging.getLogger(__name__)

# Initialize blueprint
records_blueprint = Blueprint('records', __name__, url_prefix='/api/v1/records')

# Helper function to check record access permission
def check_record_access_permission(user_id, user_role, record):
    """
    Check if a user has permission to access a record
    
    Args:
        user_id (int): ID of the user
        user_role (str): Role of the user
        record (MedicalRecord): The record to check
        
    Returns:
        bool: True if access is permitted, False otherwise
    """
    # Admin has access to all records
    if user_role == 'admin':
        return True
    
    # Patient can access their own records
    if user_role == 'patient' and record.patient_id == user_id:
        return True
    
    # Provider can access records they created
    if user_role == 'doctor' and record.provider_id == user_id:
        return True
    
    # Provider can access records of their patients (simplified logic - in a real system this would be more complex)
    if user_role == 'doctor':
        # For demonstration, we'll say all doctors can access all records
        # In a real system, this would check patient-doctor relationships
        return True
    
    # Insurance can access records they're authorized for
    if user_role == 'insurance':
        # For demonstration, we'll say insurance can access all records
        # In a real system, this would check insurance authorization
        return True
    
    return False

# Define API endpoints
@records_blueprint.route('/', methods=['GET'])
@auth_required
def get_records():
    """Get medical records"""
    try:
        # Check if a specific patient ID is provided
        patient_id = request.args.get('patient_id')
        if patient_id:
            patient_id = int(patient_id)
            
            # If requesting records for a specific patient, check permissions
            if request.user_role != 'admin' and request.user_role != 'doctor' and request.user_id != patient_id:
                return jsonify({'error': 'Not authorized to access these records'}), 403
        else:
            # If no patient ID specified, use the logged-in user's ID (if patient)
            if request.user_role == 'patient':
                patient_id = request.user_id
            else:
                # For admin, doctor, or insurance, we need a patient ID
                return jsonify({'error': 'Patient ID required'}), 400
        
        # Get records
        records = get_medical_records_for_patient(patient_id)
        
        # Format records
        record_list = []
        session = Session()
        try:
            for record in records:
                # Get provider name
                provider = session.query(User).filter(User.id == record.provider_id).first()
                provider_name = provider.full_name if provider else "Unknown"
                
                # Format record data
                record_data = {
                    'id': record.id,
                    'record_id': record.record_id,
                    'patient_id': record.patient_id,
                    'provider_id': record.provider_id,
                    'provider_name': provider_name,
                    'record_type': record.record_type,
                    'created_at': record.created_at.isoformat() if record.created_at else None,
                    'recorded_at': record.recorded_at.isoformat() if record.recorded_at else None,
                    'institution': record.institution,
                    'department': record.department,
                    'location': record.location,
                    'transaction_id': record.transaction_id,
                    'block_number': record.block_number
                }
                
                record_list.append(record_data)
                
                # Log this access
                log_record_access(
                    record_id=record.id,
                    user_id=request.user_id,
                    action='view',
                    ip_address=request.remote_addr,
                    user_agent=request.user_agent.string
                )
                
            return jsonify(record_list)
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error getting records: {str(e)}")
        return jsonify({'error': str(e)}), 500

@records_blueprint.route('/<int:record_id>', methods=['GET'])
@auth_required
def get_record(record_id):
    """Get a specific medical record with data"""
    try:
        # Get record
        session = Session()
        try:
            record = session.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
            
            if not record:
                return jsonify({'error': 'Record not found'}), 404
            
            # Check permission
            has_permission = check_record_access_permission(request.user_id, request.user_role, record)
            if not has_permission:
                return jsonify({'error': 'Not authorized to access this record'}), 403
            
            # Get provider name
            provider = session.query(User).filter(User.id == record.provider_id).first()
            provider_name = provider.full_name if provider else "Unknown"
            
            # Get patient name
            patient = session.query(User).filter(User.id == record.patient_id).first()
            patient_name = patient.full_name if patient else "Unknown"
            
            # Decrypt record data if available
            encrypted_data = record.encrypted_data
            decrypted_data = None
            
            if encrypted_data:
                # Load encryption key
                key = load_encryption_key(BLOCKCHAIN_KEY_FILE)
                if key:
                    decrypted_data = record.decrypt_data(key)
            
            # Format record data
            record_data = {
                'id': record.id,
                'record_id': record.record_id,
                'patient_id': record.patient_id,
                'patient_name': patient_name,
                'provider_id': record.provider_id,
                'provider_name': provider_name,
                'record_type': record.record_type,
                'created_at': record.created_at.isoformat() if record.created_at else None,
                'updated_at': record.updated_at.isoformat() if record.updated_at else None,
                'recorded_at': record.recorded_at.isoformat() if record.recorded_at else None,
                'institution': record.institution,
                'department': record.department,
                'location': record.location,
                'transaction_id': record.transaction_id,
                'block_number': record.block_number,
                'data': decrypted_data
            }
            
            # Log this access
            log_record_access(
                record_id=record.id,
                user_id=request.user_id,
                action='view',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string
            )
            
            return jsonify(record_data)
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error getting record: {str(e)}")
        return jsonify({'error': str(e)}), 500

@records_blueprint.route('/', methods=['POST'])
@auth_required
def create_record():
    """Create a new medical record"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['patient_id', 'record_type', 'data']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Only doctors and admins can create records
        if request.user_role not in ['doctor', 'admin']:
            return jsonify({'error': 'Only healthcare providers can create records'}), 403
        
        # Set provider ID to the logged-in user
        provider_id = request.user_id
        
        # Prepare record data
        record_data = {
            'patient_id': data['patient_id'],
            'provider_id': provider_id,
            'record_type': data['record_type'],
            'data': data['data']
        }
        
        # Add optional fields
        optional_fields = ['recorded_at', 'institution', 'department', 'location']
        for field in optional_fields:
            if field in data:
                record_data[field] = data[field]
        
        # Load encryption key
        key = load_encryption_key(BLOCKCHAIN_KEY_FILE)
        if not key:
            # Generate a new key if none exists
            from utils.helpers import generate_encryption_key, save_encryption_key
            key = generate_encryption_key()
            save_encryption_key(key, BLOCKCHAIN_KEY_FILE)
        
        # Create record
        record = create_medical_record(
            **record_data,
            encryption_key=key
        )
        
        # Log creation
        log_record_access(
            record_id=record.id,
            user_id=request.user_id,
            action='create',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        
        # TODO: Submit to blockchain
        # In a real implementation, we would submit the record to the blockchain here
        # For now, we'll just simulate by setting a transaction ID
        
        session = Session()
        try:
            record = session.query(MedicalRecord).filter(MedicalRecord.id == record.id).first()
            record.transaction_id = f"tx_{generate_unique_id()}"
            record.block_number = 12345  # Simulated block number
            session.commit()
        finally:
            session.close()
        
        return jsonify({
            'message': 'Record created successfully',
            'record_id': record.id,
            'blockchain_tx': record.transaction_id
        }), 201
        
    except Exception as e:
        logger.error(f"Error creating record: {str(e)}")
        return jsonify({'error': str(e)}), 500

@records_blueprint.route('/<int:record_id>', methods=['PUT'])
@auth_required
def update_record(record_id):
    """Update a medical record"""
    try:
        data = request.json
        
        # Get record
        session = Session()
        try:
            record = session.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
            
            if not record:
                return jsonify({'error': 'Record not found'}), 404
            
            # Only the provider who created the record or an admin can update it
            if record.provider_id != request.user_id and request.user_role != 'admin':
                return jsonify({'error': 'Not authorized to update this record'}), 403
            
            # Fields that cannot be updated
            restricted_fields = ['id', 'record_id', 'patient_id', 'provider_id', 'created_at', 
                                 'data_hash', 'transaction_id', 'block_number']
            
            # Update metadata fields
            updated_fields = []
            for key, value in data.items():
                if key not in restricted_fields and key != 'data' and hasattr(record, key):
                    setattr(record, key, value)
                    updated_fields.append(key)
            
            # Update record data if provided
            if 'data' in data:
                # Load encryption key
                key = load_encryption_key(BLOCKCHAIN_KEY_FILE)
                if not key:
                    return jsonify({'error': 'Encryption key not found'}), 500
                
                # Re-encrypt data
                success = record.encrypt_data(data['data'], key)
                if not success:
                    return jsonify({'error': 'Failed to encrypt record data'}), 500
                
                updated_fields.append('data')
                
                # TODO: Update on blockchain
                # In a real implementation, we would update the record on the blockchain here
                # For now, we'll just simulate by updating the transaction ID
                record.transaction_id = f"tx_update_{generate_unique_id()}"
            
            # Save changes
            session.commit()
            
            # Log update
            log_record_access(
                record_id=record.id,
                user_id=request.user_id,
                action='update',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string
            )
            
            return jsonify({
                'message': 'Record updated successfully',
                'updated_fields': updated_fields
            })
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error updating record: {str(e)}")
        return jsonify({'error': str(e)}), 500

@records_blueprint.route('/<int:record_id>', methods=['DELETE'])
@auth_required
def delete_record(record_id):
    """Delete a medical record (soft delete)"""
    try:
        # Get record
        session = Session()
        try:
            record = session.query(MedicalRecord).filter(MedicalRecord.id == record_id).first()
            
            if not record:
                return jsonify({'error': 'Record not found'}), 404
            
            # Only the provider who created the record or an admin can delete it
            if record.provider_id != request.user_id and request.user_role != 'admin':
                return jsonify({'error': 'Not authorized to delete this record'}), 403
            
            # Soft delete
            record.is_active = False
            
            # TODO: Mark as deleted on blockchain
            # In a real implementation, we would mark the record as deleted on the blockchain here
            
            # Save changes
            session.commit()
            
            # Log deletion
            log_record_access(
                record_id=record.id,
                user_id=request.user_id,
                action='delete',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string
            )
            
            return jsonify({
                'message': 'Record deleted successfully'
            })
            
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Error deleting record: {str(e)}")
        return jsonify({'error': str(e)}), 500 