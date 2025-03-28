"""
Unit tests for MedBlock database models

This module contains unit tests for the database models in MedBlock.
"""

import os
import sys
import unittest
import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from database.models import User, MedicalRecord, AccessLog
from utils.helpers import generate_encryption_key

class TestUserModel(unittest.TestCase):
    """Tests for the User model"""
    
    def test_user_init(self):
        """Test User initialization"""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hash",
            first_name="Test",
            last_name="User",
            role="patient"
        )
        
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.password_hash, "hash")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.role, "patient")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_verified)
    
    def test_full_name_property(self):
        """Test full_name property"""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hash",
            first_name="Test",
            last_name="User",
            role="patient"
        )
        
        self.assertEqual(user.full_name, "Test User")
    
    def test_age_property(self):
        """Test age property"""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hash",
            first_name="Test",
            last_name="User",
            role="patient",
            date_of_birth=datetime.datetime(1990, 1, 1)
        )
        
        # Age will depend on the current date
        today = datetime.datetime.utcnow().date()
        expected_age = today.year - 1990 - ((today.month, today.day) < (1, 1))
        
        self.assertEqual(user.age, expected_age)
    
    def test_calculate_bmi(self):
        """Test BMI calculation"""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hash",
            first_name="Test",
            last_name="User",
            role="patient",
            height=180,  # cm
            weight=80    # kg
        )
        
        bmi = user.calculate_bmi()
        self.assertAlmostEqual(bmi, 24.69, places=2)
        self.assertAlmostEqual(user.bmi, 24.69, places=2)


class TestMedicalRecordModel(unittest.TestCase):
    """Tests for the MedicalRecord model"""
    
    def test_medical_record_init(self):
        """Test MedicalRecord initialization"""
        record = MedicalRecord(
            record_id="record123",
            patient_id=1,
            provider_id=2,
            record_type="consultation",
            recorded_at=datetime.datetime(2023, 1, 1),
            data_hash="hash123"
        )
        
        self.assertEqual(record.record_id, "record123")
        self.assertEqual(record.patient_id, 1)
        self.assertEqual(record.provider_id, 2)
        self.assertEqual(record.record_type, "consultation")
        self.assertEqual(record.recorded_at, datetime.datetime(2023, 1, 1))
        self.assertEqual(record.data_hash, "hash123")
        self.assertTrue(record.is_active)
        self.assertTrue(record.is_verified)
    
    def test_encrypt_decrypt_data(self):
        """Test data encryption and decryption"""
        record = MedicalRecord(
            record_id="record123",
            patient_id=1,
            provider_id=2,
            record_type="consultation",
            recorded_at=datetime.datetime(2023, 1, 1)
        )
        
        # Test data
        test_data = {
            "notes": "Patient reports feeling well",
            "vitals": {
                "temperature": 36.8,
                "heart_rate": 72
            }
        }
        
        # Generate encryption key
        key = generate_encryption_key()
        
        # Encrypt data
        success = record.encrypt_data(test_data, key)
        self.assertTrue(success)
        self.assertIsNotNone(record.data_hash)
        self.assertIsNotNone(record.encrypted_data)
        
        # Decrypt data
        decrypted_data = record.decrypt_data(key)
        self.assertEqual(decrypted_data, test_data)


class TestAccessLogModel(unittest.TestCase):
    """Tests for the AccessLog model"""
    
    def test_access_log_init(self):
        """Test AccessLog initialization"""
        log = AccessLog(
            record_id=1,
            user_id=2,
            action="view",
            ip_address="192.168.1.1",
            user_agent="Mozilla/5.0"
        )
        
        self.assertEqual(log.record_id, 1)
        self.assertEqual(log.user_id, 2)
        self.assertEqual(log.action, "view")
        self.assertEqual(log.ip_address, "192.168.1.1")
        self.assertEqual(log.user_agent, "Mozilla/5.0")
        self.assertTrue(log.is_authorized)
        self.assertFalse(log.is_anomalous)


if __name__ == "__main__":
    unittest.main() 