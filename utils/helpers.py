"""
Helper Utility Functions for MedBlock

This module provides various utility functions used throughout the MedBlock system.
"""

import os
import sys
import uuid
import hashlib
import datetime
import secrets
import re
from cryptography.fernet import Fernet

def generate_unique_id():
    """
    Generate a unique ID for records
    
    Returns:
        str: Unique ID
    """
    return str(uuid.uuid4())

def hash_password(password):
    """
    Hash a password for storing in the database
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    # In a real system, you would use a secure password hashing algorithm like bcrypt
    # This is just a simple example using SHA-256
    salt = secrets.token_hex(16)
    hash_obj = hashlib.sha256((password + salt).encode())
    return f"{salt}${hash_obj.hexdigest()}"

def verify_password(stored_password, provided_password):
    """
    Verify a password against its hash
    
    Args:
        stored_password (str): Stored hashed password
        provided_password (str): Plain text password to verify
        
    Returns:
        bool: True if password matches, False otherwise
    """
    salt, hash_value = stored_password.split('$')
    hash_obj = hashlib.sha256((provided_password + salt).encode())
    return hash_obj.hexdigest() == hash_value

def generate_encryption_key():
    """
    Generate a new Fernet encryption key
    
    Returns:
        bytes: Encryption key
    """
    return Fernet.generate_key()

def save_encryption_key(key, filename='encryption_key.key'):
    """
    Save an encryption key to a file
    
    Args:
        key (bytes): Encryption key
        filename (str): File to save the key to
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'wb') as key_file:
            key_file.write(key)
        os.chmod(filename, 0o600)  # Restrict permissions to owner only
        return True
    except Exception as e:
        print(f"Error saving key: {str(e)}")
        return False

def load_encryption_key(filename='encryption_key.key'):
    """
    Load an encryption key from a file
    
    Args:
        filename (str): File to load the key from
        
    Returns:
        bytes: Encryption key or None if file doesn't exist
    """
    try:
        with open(filename, 'rb') as key_file:
            return key_file.read()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error loading key: {str(e)}")
        return None

def format_datetime(dt):
    """
    Format a datetime object for display
    
    Args:
        dt (datetime): Datetime object
        
    Returns:
        str: Formatted date and time
    """
    if not dt:
        return ""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def parse_datetime(dt_str):
    """
    Parse a datetime string
    
    Args:
        dt_str (str): Datetime string
        
    Returns:
        datetime: Parsed datetime object or None if invalid
    """
    try:
        return datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        try:
            return datetime.datetime.strptime(dt_str, "%Y-%m-%d")
        except (ValueError, TypeError):
            return None

def is_valid_email(email):
    """
    Check if an email address is valid
    
    Args:
        email (str): Email address
        
    Returns:
        bool: True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def get_age_from_dob(dob):
    """
    Calculate age from date of birth
    
    Args:
        dob (datetime): Date of birth
        
    Returns:
        int: Age in years
    """
    if not dob:
        return None
        
    today = datetime.datetime.utcnow().date()
    born = dob.date() if isinstance(dob, datetime.datetime) else dob
    
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def is_valid_password(password):
    """
    Check if a password meets the security requirements
    
    Args:
        password (str): Password
        
    Returns:
        bool: True if valid, False otherwise
    """
    # At least 8 characters, containing uppercase, lowercase, digit, and special character
    if len(password) < 8:
        return False
        
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        else:
            has_special = True
    
    return has_upper and has_lower and has_digit and has_special 