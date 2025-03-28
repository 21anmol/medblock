"""
Database Utility Functions for MedBlock

This module provides utility functions for database operations.
"""

import os
import sys
import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.models import Session, User, MedicalRecord, AccessLog
from utils.helpers import generate_unique_id

def create_user(username, email, password_hash, first_name, last_name, role, **kwargs):
    """
    Create a new user in the database
    
    Args:
        username (str): Username for the user
        email (str): Email address
        password_hash (str): Hashed password
        first_name (str): First name
        last_name (str): Last name
        role (str): User role (patient, doctor, admin, insurance)
        **kwargs: Additional user fields
        
    Returns:
        User: Created user object
    """
    session = Session()
    try:
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=role,
            **kwargs
        )
        session.add(user)
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_user_by_id(user_id):
    """
    Get a user by ID
    
    Args:
        user_id (int): User ID
        
    Returns:
        User: User object if found, None otherwise
    """
    session = Session()
    try:
        return session.query(User).filter(User.id == user_id).first()
    finally:
        session.close()

def get_user_by_username(username):
    """
    Get a user by username
    
    Args:
        username (str): Username
        
    Returns:
        User: User object if found, None otherwise
    """
    session = Session()
    try:
        return session.query(User).filter(User.username == username).first()
    finally:
        session.close()

def create_medical_record(patient_id, provider_id, record_type, data, encryption_key, recorded_at=None, **kwargs):
    """
    Create a new medical record
    
    Args:
        patient_id (int): ID of the patient
        provider_id (int): ID of the provider creating the record
        record_type (str): Type of medical record
        data (dict): Record data
        encryption_key (bytes): Key for encrypting the data
        recorded_at (datetime, optional): When the medical event occurred
        **kwargs: Additional record fields
        
    Returns:
        MedicalRecord: Created record object
    """
    session = Session()
    try:
        if recorded_at is None:
            recorded_at = datetime.datetime.utcnow()
            
        record = MedicalRecord(
            record_id=generate_unique_id(),
            patient_id=patient_id,
            provider_id=provider_id,
            record_type=record_type,
            recorded_at=recorded_at,
            **kwargs
        )
        
        # Encrypt the data
        success = record.encrypt_data(data, encryption_key)
        if not success:
            raise ValueError("Failed to encrypt record data")
        
        session.add(record)
        session.commit()
        return record
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_medical_records_for_patient(patient_id):
    """
    Get all medical records for a patient
    
    Args:
        patient_id (int): ID of the patient
        
    Returns:
        list: List of medical records
    """
    session = Session()
    try:
        return session.query(MedicalRecord).filter(
            MedicalRecord.patient_id == patient_id,
            MedicalRecord.is_active == True
        ).order_by(MedicalRecord.recorded_at.desc()).all()
    finally:
        session.close()

def log_record_access(record_id, user_id, action, ip_address=None, user_agent=None, is_authorized=True):
    """
    Log access to a medical record
    
    Args:
        record_id (int): ID of the accessed record
        user_id (int): ID of the user accessing the record
        action (str): Action performed (view, create, update, delete)
        ip_address (str, optional): IP address of the request
        user_agent (str, optional): User agent of the request
        is_authorized (bool): Whether the access was authorized
        
    Returns:
        AccessLog: Created log object
    """
    session = Session()
    try:
        log = AccessLog(
            record_id=record_id,
            user_id=user_id,
            action=action,
            ip_address=ip_address,
            user_agent=user_agent,
            is_authorized=is_authorized
        )
        session.add(log)
        session.commit()
        return log
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def get_recent_access_logs(limit=100):
    """
    Get the most recent access logs
    
    Args:
        limit (int): Maximum number of logs to return
        
    Returns:
        list: List of access logs
    """
    session = Session()
    try:
        return session.query(AccessLog).order_by(
            AccessLog.access_time.desc()
        ).limit(limit).all()
    finally:
        session.close()

def get_anomalous_access_logs(limit=100):
    """
    Get access logs marked as anomalous
    
    Args:
        limit (int): Maximum number of logs to return
        
    Returns:
        list: List of anomalous access logs
    """
    session = Session()
    try:
        return session.query(AccessLog).filter(
            AccessLog.is_anomalous == True
        ).order_by(AccessLog.access_time.desc()).limit(limit).all()
    finally:
        session.close() 