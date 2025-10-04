import uuid

from .database import db
class Doctor:
    def __init__(self, doctor_id=None, user_id=None, organization_id=None, specialization=None, license_number=None):
        self.doctor_id = doctor_id if doctor_id else uuid.uuid4().hex
        self.user_id = user_id
        self.organization_id = organization_id
        self.specialization = specialization
        self.license_number = license_number
        self._db = db

    def __is_doctor_in_org(self):
        """
        Checks if the doctor is already registered in the organization.
        Returns:
            bool: True if the doctor is already registered, False otherwise.
        """
        doctor_list = self._db.get_doctor_by_user_id(self.user_id)
        doctor_org_id_list = [doctor['organization_id'] for doctor in doctor_list]
        if (doctor_org_id_list) and (self.organization_id in doctor_org_id_list):
            return True
        return False
    
    def register(self):
        """
        Registers a new doctor.
        Returns:
            tuple: A tuple containing a boolean and a value:
                - (False, None): If the doctor already exists.
                - (True, doctor_id): If the doctor is successfully registered.
        """
        if self.__is_doctor_in_org():
            return False, None
        doctor_id = self._db.create_doctor(self.doctor_id, self.user_id, self.organization_id, self.specialization, self.license_number)
        return True, doctor_id
    
    def get_doctor_organization_by_user_id(self):
        """
        Gets the organization of the doctor.
        Returns:
            dict: The organization details if found, None otherwise.
        """
        org_list = self._db.get_doctor_organization(self.user_id)
        return org_list