import json
import os
from web3 import Web3
from cryptography.fernet import Fernet
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("blockchain.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BlockchainIntegration:
    """
    Integration with blockchain for storing and retrieving medical records
    with role-based access control
    """
    
    def __init__(self, provider_url=None, contract_address=None, keyfile=None):
        """
        Initialize blockchain connection
        
        Args:
            provider_url (str): URL of the blockchain provider
            contract_address (str): Address of the deployed smart contract
            keyfile (str): Path to the encryption key file
        """
        # Default to local development chain if no provider URL is provided
        self.provider_url = provider_url or "http://localhost:8545"
        
        try:
            self.web3 = Web3(Web3.HTTPProvider(self.provider_url))
            if self.web3.is_connected():
                logger.info(f"Connected to Ethereum node at {self.provider_url}")
            else:
                logger.warning(f"Failed to connect to Ethereum node at {self.provider_url}")
        except Exception as e:
            logger.error(f"Error connecting to blockchain: {str(e)}")
            self.web3 = None
        
        self.contract_address = contract_address
        self.contract = None
        
        # Load contract ABI if contract address is provided
        if contract_address and self.web3 and self.web3.is_connected():
            self._load_contract()
        
        # Initialize encryption key
        self.key = None
        if keyfile and os.path.exists(keyfile):
            with open(keyfile, 'rb') as f:
                self.key = f.read()
        else:
            # Generate a new key if none is provided
            self.key = Fernet.generate_key()
            if keyfile:
                with open(keyfile, 'wb') as f:
                    f.write(self.key)
        
        self.cipher = Fernet(self.key)
    
    def _load_contract(self):
        """Load the smart contract from its ABI"""
        try:
            # Load ABI from file
            abi_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'abi/MedicalRecords.json')
            with open(abi_path, 'r') as f:
                contract_abi = json.load(f)
            
            # Initialize contract
            self.contract = self.web3.eth.contract(
                address=self.contract_address,
                abi=contract_abi
            )
            logger.info(f"Contract loaded at address {self.contract_address}")
        except Exception as e:
            logger.error(f"Error loading contract: {str(e)}")
            self.contract = None
    
    def deploy_contract(self, account_address, private_key):
        """
        Deploy the medical records smart contract
        
        Args:
            account_address (str): Address of the account deploying the contract
            private_key (str): Private key of the account
            
        Returns:
            str: Address of the deployed contract
        """
        if not self.web3 or not self.web3.is_connected():
            raise ConnectionError("Not connected to blockchain")
        
        try:
            # Load contract bytecode and ABI
            contract_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'abi/MedicalRecords.json')
            with open(contract_path, 'r') as f:
                contract_data = json.load(f)
            
            # Create contract object
            MedicalRecords = self.web3.eth.contract(
                abi=contract_data['abi'],
                bytecode=contract_data['bytecode']
            )
            
            # Build transaction
            nonce = self.web3.eth.get_transaction_count(account_address)
            transaction = MedicalRecords.constructor().build_transaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.web3.to_wei('50', 'gwei')
            })
            
            # Sign and send transaction
            signed_tx = self.web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for transaction receipt
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            contract_address = tx_receipt['contractAddress']
            
            # Update contract address and load the contract
            self.contract_address = contract_address
            self._load_contract()
            
            logger.info(f"Contract deployed at address {contract_address}")
            return contract_address
        except Exception as e:
            logger.error(f"Error deploying contract: {str(e)}")
            raise
    
    def add_patient(self, account_address, private_key, patient_id, patient_address, name, dob):
        """
        Add a new patient to the system
        
        Args:
            account_address (str): Address of the admin account
            private_key (str): Private key of the admin account
            patient_id (str): Unique ID for the patient
            patient_address (str): Ethereum address of the patient
            name (str): Patient's name (will be encrypted)
            dob (str): Patient's date of birth (will be encrypted)
            
        Returns:
            dict: Transaction details
        """
        if not self.web3 or not self.contract:
            raise ConnectionError("Blockchain or contract not initialized")
        
        try:
            # Encrypt sensitive information
            encrypted_name = self.encrypt(name)
            encrypted_dob = self.encrypt(dob)
            
            # Build transaction
            nonce = self.web3.eth.get_transaction_count(account_address)
            transaction = self.contract.functions.addPatient(
                patient_id,
                patient_address,
                encrypted_name,
                encrypted_dob
            ).build_transaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 500000,
                'gasPrice': self.web3.to_wei('50', 'gwei')
            })
            
            # Sign and send transaction
            signed_tx = self.web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for transaction receipt
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
            logger.info(f"Patient {patient_id} added successfully")
            return {
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber'],
                'status': 'success' if tx_receipt['status'] == 1 else 'failed'
            }
        except Exception as e:
            logger.error(f"Error adding patient: {str(e)}")
            raise
    
    def add_medical_record(self, account_address, private_key, patient_id, record_id, record_type, data, timestamp=None):
        """
        Add a medical record for a patient
        
        Args:
            account_address (str): Address of the healthcare provider
            private_key (str): Private key of the healthcare provider
            patient_id (str): ID of the patient
            record_id (str): Unique ID for the record
            record_type (str): Type of medical record
            data (dict): Medical record data (will be encrypted)
            timestamp (str, optional): Timestamp of the record
            
        Returns:
            dict: Transaction details
        """
        if not self.web3 or not self.contract:
            raise ConnectionError("Blockchain or contract not initialized")
        
        try:
            # Convert data to JSON and encrypt
            json_data = json.dumps(data)
            encrypted_data = self.encrypt(json_data)
            
            # Use current time if timestamp not provided
            if not timestamp:
                timestamp = datetime.now().isoformat()
            
            # Build transaction
            nonce = self.web3.eth.get_transaction_count(account_address)
            transaction = self.contract.functions.addMedicalRecord(
                patient_id,
                record_id,
                record_type,
                encrypted_data,
                timestamp
            ).build_transaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 1000000,
                'gasPrice': self.web3.to_wei('50', 'gwei')
            })
            
            # Sign and send transaction
            signed_tx = self.web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for transaction receipt
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
            logger.info(f"Medical record {record_id} added for patient {patient_id}")
            return {
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber'],
                'status': 'success' if tx_receipt['status'] == 1 else 'failed'
            }
        except Exception as e:
            logger.error(f"Error adding medical record: {str(e)}")
            raise
    
    def get_medical_record(self, patient_id, record_id):
        """
        Retrieve a medical record for a patient
        
        Args:
            patient_id (str): ID of the patient
            record_id (str): ID of the record to retrieve
            
        Returns:
            dict: Medical record data (decrypted)
        """
        if not self.web3 or not self.contract:
            raise ConnectionError("Blockchain or contract not initialized")
        
        try:
            # Call the contract to get the record
            record = self.contract.functions.getMedicalRecord(patient_id, record_id).call()
            
            # Parse and decrypt the record data
            record_type, encrypted_data, timestamp, provider = record
            
            # Decrypt data
            json_data = self.decrypt(encrypted_data)
            data = json.loads(json_data)
            
            return {
                'patient_id': patient_id,
                'record_id': record_id,
                'record_type': record_type,
                'data': data,
                'timestamp': timestamp,
                'provider': provider
            }
        except Exception as e:
            logger.error(f"Error retrieving medical record: {str(e)}")
            raise
    
    def grant_access(self, account_address, private_key, patient_id, provider_address, access_level, expiry=None):
        """
        Grant access to a provider for a patient's records
        
        Args:
            account_address (str): Address of the patient or admin
            private_key (str): Private key of the patient or admin
            patient_id (str): ID of the patient
            provider_address (str): Address of the healthcare provider
            access_level (int): Level of access (1: Read, 2: Write, 3: Admin)
            expiry (int, optional): Unix timestamp for access expiry
            
        Returns:
            dict: Transaction details
        """
        if not self.web3 or not self.contract:
            raise ConnectionError("Blockchain or contract not initialized")
        
        try:
            # Set default expiry to 30 days if not provided
            if not expiry:
                expiry = int((datetime.now().timestamp() + 2592000))  # 30 days in seconds
            
            # Build transaction
            nonce = self.web3.eth.get_transaction_count(account_address)
            transaction = self.contract.functions.grantAccess(
                patient_id,
                provider_address,
                access_level,
                expiry
            ).build_transaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 500000,
                'gasPrice': self.web3.to_wei('50', 'gwei')
            })
            
            # Sign and send transaction
            signed_tx = self.web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for transaction receipt
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
            logger.info(f"Access granted to provider {provider_address} for patient {patient_id}")
            return {
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber'],
                'status': 'success' if tx_receipt['status'] == 1 else 'failed'
            }
        except Exception as e:
            logger.error(f"Error granting access: {str(e)}")
            raise
    
    def revoke_access(self, account_address, private_key, patient_id, provider_address):
        """
        Revoke a provider's access to a patient's records
        
        Args:
            account_address (str): Address of the patient or admin
            private_key (str): Private key of the patient or admin
            patient_id (str): ID of the patient
            provider_address (str): Address of the healthcare provider
            
        Returns:
            dict: Transaction details
        """
        if not self.web3 or not self.contract:
            raise ConnectionError("Blockchain or contract not initialized")
        
        try:
            # Build transaction
            nonce = self.web3.eth.get_transaction_count(account_address)
            transaction = self.contract.functions.revokeAccess(
                patient_id,
                provider_address
            ).build_transaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 500000,
                'gasPrice': self.web3.to_wei('50', 'gwei')
            })
            
            # Sign and send transaction
            signed_tx = self.web3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
            
            # Wait for transaction receipt
            tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            
            logger.info(f"Access revoked for provider {provider_address} to patient {patient_id}")
            return {
                'transaction_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber'],
                'status': 'success' if tx_receipt['status'] == 1 else 'failed'
            }
        except Exception as e:
            logger.error(f"Error revoking access: {str(e)}")
            raise
    
    def check_access(self, provider_address, patient_id):
        """
        Check if a provider has access to a patient's records
        
        Args:
            provider_address (str): Address of the healthcare provider
            patient_id (str): ID of the patient
            
        Returns:
            dict: Access details
        """
        if not self.web3 or not self.contract:
            raise ConnectionError("Blockchain or contract not initialized")
        
        try:
            # Call the contract to check access
            has_access, access_level, expiry = self.contract.functions.checkAccess(provider_address, patient_id).call()
            
            return {
                'has_access': has_access,
                'access_level': access_level,
                'expiry': expiry,
                'expired': expiry < datetime.now().timestamp() if expiry > 0 else False
            }
        except Exception as e:
            logger.error(f"Error checking access: {str(e)}")
            raise
    
    def encrypt(self, data):
        """
        Encrypt data using Fernet symmetric encryption
        
        Args:
            data (str): Data to encrypt
            
        Returns:
            str: Encrypted data in base64
        """
        if isinstance(data, str):
            data = data.encode()
        encrypted = self.cipher.encrypt(data)
        return encrypted.decode()
    
    def decrypt(self, encrypted_data):
        """
        Decrypt data using Fernet symmetric encryption
        
        Args:
            encrypted_data (str): Encrypted data in base64
            
        Returns:
            str: Decrypted data
        """
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        decrypted = self.cipher.decrypt(encrypted_data)
        return decrypted.decode()


# Example of a smart contract interface (this would be compiled separately)
CONTRACT_INTERFACE = """
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MedicalRecords {
    struct Patient {
        string id;
        address patientAddress;
        string encryptedName;
        string encryptedDOB;
        bool exists;
    }
    
    struct MedicalRecord {
        string recordType;
        string encryptedData;
        string timestamp;
        address provider;
        bool exists;
    }
    
    struct Access {
        uint8 accessLevel; // 1: Read, 2: Write, 3: Admin
        uint256 expiry;
        bool exists;
    }
    
    // Administrator of the contract
    address public admin;
    
    // Mapping of patient ID to patient data
    mapping(string => Patient) private patients;
    
    // Mapping of patient ID to record ID to medical record
    mapping(string => mapping(string => MedicalRecord)) private records;
    
    // Mapping of provider address to patient ID to access rights
    mapping(address => mapping(string => Access)) private accessRights;
    
    // Events
    event PatientAdded(string patientId, address patientAddress);
    event MedicalRecordAdded(string patientId, string recordId, string recordType);
    event AccessGranted(string patientId, address provider, uint8 accessLevel, uint256 expiry);
    event AccessRevoked(string patientId, address provider);
    
    // Modifiers
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can perform this action");
        _;
    }
    
    modifier onlyAuthorized(string memory patientId, uint8 requiredLevel) {
        require(
            msg.sender == admin || 
            msg.sender == patients[patientId].patientAddress ||
            (accessRights[msg.sender][patientId].exists && 
             accessRights[msg.sender][patientId].accessLevel >= requiredLevel &&
             accessRights[msg.sender][patientId].expiry > block.timestamp),
            "Not authorized"
        );
        _;
    }
    
    // Constructor
    constructor() {
        admin = msg.sender;
    }
    
    // Add a new patient
    function addPatient(
        string memory patientId,
        address patientAddress,
        string memory encryptedName,
        string memory encryptedDOB
    ) public onlyAdmin {
        require(!patients[patientId].exists, "Patient already exists");
        
        patients[patientId] = Patient({
            id: patientId,
            patientAddress: patientAddress,
            encryptedName: encryptedName,
            encryptedDOB: encryptedDOB,
            exists: true
        });
        
        emit PatientAdded(patientId, patientAddress);
    }
    
    // Add a medical record
    function addMedicalRecord(
        string memory patientId,
        string memory recordId,
        string memory recordType,
        string memory encryptedData,
        string memory timestamp
    ) public onlyAuthorized(patientId, 2) {
        require(patients[patientId].exists, "Patient does not exist");
        require(!records[patientId][recordId].exists, "Record already exists");
        
        records[patientId][recordId] = MedicalRecord({
            recordType: recordType,
            encryptedData: encryptedData,
            timestamp: timestamp,
            provider: msg.sender,
            exists: true
        });
        
        emit MedicalRecordAdded(patientId, recordId, recordType);
    }
    
    // Get a medical record
    function getMedicalRecord(string memory patientId, string memory recordId)
        public
        view
        onlyAuthorized(patientId, 1)
        returns (string memory, string memory, string memory, address)
    {
        require(patients[patientId].exists, "Patient does not exist");
        require(records[patientId][recordId].exists, "Record does not exist");
        
        MedicalRecord memory record = records[patientId][recordId];
        return (record.recordType, record.encryptedData, record.timestamp, record.provider);
    }
    
    // Grant access to a provider
    function grantAccess(string memory patientId, address provider, uint8 accessLevel, uint256 expiry)
        public
        onlyAuthorized(patientId, 3)
    {
        require(patients[patientId].exists, "Patient does not exist");
        require(accessLevel >= 1 && accessLevel <= 3, "Invalid access level");
        require(expiry > block.timestamp, "Expiry must be in the future");
        
        accessRights[provider][patientId] = Access({
            accessLevel: accessLevel,
            expiry: expiry,
            exists: true
        });
        
        emit AccessGranted(patientId, provider, accessLevel, expiry);
    }
    
    // Revoke access from a provider
    function revokeAccess(string memory patientId, address provider)
        public
        onlyAuthorized(patientId, 3)
    {
        require(patients[patientId].exists, "Patient does not exist");
        require(accessRights[provider][patientId].exists, "No access rights to revoke");
        
        delete accessRights[provider][patientId];
        
        emit AccessRevoked(patientId, provider);
    }
    
    // Check if a provider has access to a patient's records
    function checkAccess(address provider, string memory patientId)
        public
        view
        returns (bool, uint8, uint256)
    {
        if (!accessRights[provider][patientId].exists) {
            return (false, 0, 0);
        }
        
        Access memory access = accessRights[provider][patientId];
        bool hasAccess = access.exists && access.expiry > block.timestamp;
        
        return (hasAccess, access.accessLevel, access.expiry);
    }
}
"""

if __name__ == "__main__":
    # Example usage
    blockchain = BlockchainIntegration(
        provider_url="http://localhost:8545",
        keyfile="encryption_key.key"
    )
    
    print("Blockchain integration initialized")
    
    # Note: In a real application, you would need to:
    # 1. Deploy the contract using the deploy_contract method
    # 2. Use the contract to manage patients and medical records
    # 3. Implement proper key management for encryption 