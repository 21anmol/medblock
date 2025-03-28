"""
User Model for MedBlock

This module defines the User model for the MedBlock system.
"""

import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    """User model representing users in the MedBlock system."""
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    
    # Blockchain address for this user
    blockchain_address = Column(String(64), unique=True, nullable=True)
    
    # User role (patient, doctor, admin, insurance)
    role = Column(Enum('patient', 'doctor', 'admin', 'insurance', name='user_roles'), nullable=False)
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Patient-specific fields
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(Enum('male', 'female', 'other', name='gender_types'), nullable=True)
    blood_type = Column(Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-', name='blood_types'), nullable=True)
    
    # Additional health metrics
    height = Column(Float, nullable=True)  # in cm
    weight = Column(Float, nullable=True)  # in kg
    bmi = Column(Float, nullable=True)
    
    # Contact information
    phone_number = Column(String(20), nullable=True)
    address = Column(String(200), nullable=True)
    city = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    country = Column(String(50), nullable=True)
    zip_code = Column(String(20), nullable=True)
    
    def __repr__(self):
        """Return string representation of the model."""
        return f"<User(id={self.id}, username='{self.username}', role='{self.role}')>"
    
    @property
    def full_name(self):
        """Return user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        """Calculate user's age based on date of birth."""
        if self.date_of_birth:
            today = datetime.datetime.utcnow().date()
            born = self.date_of_birth.date()
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return None
    
    def calculate_bmi(self):
        """Calculate BMI if height and weight are available."""
        if self.height and self.weight and self.height > 0:
            # BMI = weight(kg) / (height(m))^2
            height_in_meters = self.height / 100
            bmi = self.weight / (height_in_meters ** 2)
            self.bmi = round(bmi, 2)
            return self.bmi
        return None 