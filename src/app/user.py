from .database import db
import uuid
import hashlib


class User:
    def __init__(self, user_id=None, email=None, password=None, name=None, is_admin=False, phone_number=None, adhaar_number=None, dob=None, gender=None, chronic_diseases=None):
        self.user_id = uuid.uuid4().hex if user_id is None else user_id
        self.email = email
        self.password = password
        self.name = name
        self.is_admin = is_admin
        self.phone_number = phone_number
        self.adhaar_number = adhaar_number
        self.dob = dob
        self.gender = gender
        self.chronic_diseases = chronic_diseases
        self._db = db

    def _check_password(self, stored_password_hash, provided_password):
        return self._hash_password(provided_password) == stored_password_hash
    
    def _hash_password(self,password):
        password_bytes = password.encode('utf-8')
        hash_object = hashlib.sha256(password_bytes)
        return str(hash_object.hexdigest())
    
    def isUserValid(self) -> tuple[bool, int]:
        """
        Validates the user's credentials.

        Returns:
            tuple: A tuple containing a boolean and a value:
                - (False, None): If the user does not exist or the password is invalid.
                - (True, user_id): If the user exists and the password is valid.
        """
        user = self._db.get_user_by_email(self.email)
        if not user:
            return False, None
        if not self._check_password(user['password_hash'], self.password):
            return False, None
        check, doctor_id = self.is_user_doctor(user['user_id'])
        if check:
            user['doctor_id'] = doctor_id
            return True, user['user_id'], user['doctor_id']
        return True, user['user_id'], None
    
    def create(self) -> tuple[bool, str]:
        """
        Creats a new user.
        Returns:
            tuple: A tuple containing a boolean and a value:
                - (False, None): If the user already exists.
                - (True, user_id): If the user is successfully created.
        """
        if self._db.get_user_by_email(self.email):
            return False, None
        hashed_password = self._hash_password(self.password)
        user_id = self._db.create_user(self.user_id, self.email, hashed_password, self.name, self.is_admin, self.phone_number, self.adhaar_number, self.dob, self.gender, self.chronic_diseases)
        return True, user_id
    
    def get_user_id_by_email(self) -> str:
        """
        Gets user id by email
        Returns:
            tuple: A tuple containing a boolean and a value:
                - (False, None): If the user doesn't exists.
                - (True, user_id): If the user exists.
        """
        user = self._db.get_user_by_email(self.email)
        if not user:
            return False, None
        return True, user['user_id']
    
    def get_user(self) -> dict:
        """
        Gets user details by user id.
        Returns:
            dict: The user details if found, None otherwise.
        """
        return self._db.get_user_by_id(self.user_id)
    
    def get_user_patient_data(self) -> dict:
        """
        Gets patients details
        Returns:
            dict: The user details if found, None otherwise.
        """
        return self._db.get_user_patient_data(self.email)
    
    def is_user_doctor(self, user_id: str) -> tuple[bool, str]:
        """
        Checks if the user is a doctor.
        
        :param user_id: The ID of the user to check.
        :return: A tuple containing a boolean indicating if the user is a doctor and the doctor's ID if they are.
        """
        doctor = self._db.get_doctor_by_user_id(user_id)
        if doctor:
            return True, doctor[0]['doctor_id']
        return False, None