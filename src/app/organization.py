from .database import db
import uuid
class Organization:
    def __init__(self,id=None, name=None, license_number=None, address=None, contact_number=None, admin_id=None):
        self.id = id if id else uuid.uuid4().hex
        self.name = name
        self.license_number = license_number
        self.address = address
        self.contact_number = contact_number
        self.admin_id = admin_id
        self._db = db

    def create(self) -> tuple[bool, str]:
        """
        Creates a new organization.
        Returns:
            tuple: A tuple containing a boolean and a value:
                - (False, None): If the organization already exists.
                - (True, organization_id): If the organization is successfully created.
        """
        if self._db.get_organization_by_license(self.license_number):
            return False, None
        organization_id = self._db.create_organization(self.id, self.name, self.license_number, self.address, self.contact_number, self.admin_id)
        return True, organization_id