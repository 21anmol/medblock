"""
Medical Record Model for MedBlock

This module defines the MedicalRecord model for the MedBlock system.
"""

import datetime
import json
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()

class MedicalRecord(Base):
    """Medical record model for storing patient health records"""
    
    __tablename__ = 'medical_records'
    
    id = Column(Integer, primary_key=True)
    record_id = Column(String(64), unique=True, nullable=False)  # Blockchain identifier
    
    # Foreign key to patient
    patient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    patient = relationship('User', foreign_keys=[patient_id])
    
    # Foreign key to provider who created the record
    provider_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    provider = relationship('User', foreign_keys=[provider_id])
    
    # Record type
    record_type = Column(Enum(
        'consultation', 
        'lab_result', 
        'imaging', 
        'prescription', 
        'vaccination', 
        'surgery', 
        'allergy', 
        'diagnosis',
        'treatment_plan',
        name='record_types'
    ), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    recorded_at = Column(DateTime, nullable=False)  # When the medical event occurred
    
    # Record data - encrypted on blockchain, this is a reference
    data_hash = Column(String(128), nullable=False)  # Hash of the data on the blockchain
    encrypted_data = Column(Text, nullable=True)  # Encrypted data if stored in DB
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=True)
    
    # Blockchain transaction ID
    transaction_id = Column(String(128), nullable=True)
    block_number = Column(Integer, nullable=True)
    
    # Additional metadata
    institution = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    
    def __repr__(self):
        """Return string representation of the record"""
        return f"<MedicalRecord(id={self.id}, type='{self.record_type}', patient_id={self.patient_id})>"

    @hybrid_property
    def age_at_record(self):
        """Calculate patient's age at the time of the record"""
        if self.patient and self.patient.date_of_birth and self.recorded_at:
            born = self.patient.date_of_birth.date()
            record_date = self.recorded_at.date()
            return record_date.year - born.year - ((record_date.month, record_date.day) < (born.month, born.day))
        return None
    
    def decrypt_data(self, decryption_key):
        """Decrypt the medical record data using the provided key"""
        if not self.encrypted_data:
            return None
        
        try:
            # In a real implementation, this would use a proper encryption library
            # This is just a placeholder
            import base64
            from cryptography.fernet import Fernet
            
            cipher = Fernet(decryption_key)
            decrypted_data = cipher.decrypt(self.encrypted_data.encode())
            return json.loads(decrypted_data.decode())
        except Exception as e:
            print(f"Error decrypting data: {str(e)}")
            return None
    
    def encrypt_data(self, data, encryption_key):
        """Encrypt the medical record data using the provided key"""
        try:
            # In a real implementation, this would use a proper encryption library
            # This is just a placeholder
            import base64
            import hashlib
            from cryptography.fernet import Fernet
            
            # Convert data to JSON string
            data_str = json.dumps(data)
            
            # Calculate hash
            hash_obj = hashlib.sha256(data_str.encode())
            self.data_hash = hash_obj.hexdigest()
            
            # Encrypt data
            cipher = Fernet(encryption_key)
            self.encrypted_data = cipher.encrypt(data_str.encode()).decode()
            
            return True
        except Exception as e:
            print(f"Error encrypting data: {str(e)}")
            return False


class AccessLog(Base):
    """Log of access to medical records"""
    
    __tablename__ = 'access_logs'
    
    id = Column(Integer, primary_key=True)
    
    # Foreign key to record and user
    record_id = Column(Integer, ForeignKey('medical_records.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Access information
    access_time = Column(DateTime, default=datetime.datetime.utcnow)
    ip_address = Column(String(45), nullable=True)  # IPv6 addresses are longer
    user_agent = Column(String(255), nullable=True)
    action = Column(Enum('view', 'create', 'update', 'delete', name='access_actions'), nullable=False)
    
    # Success status
    is_authorized = Column(Boolean, default=True)
    is_anomalous = Column(Boolean, default=False)
    anomaly_score = Column(Float, nullable=True)
    
    def __repr__(self):
        """Return string representation of the access log"""
        return f"<AccessLog(id={self.id}, record_id={self.record_id}, user_id={self.user_id}, action='{self.action}')>" 