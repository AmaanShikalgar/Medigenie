import psycopg2
from dotenv import load_dotenv
load_dotenv()
import json
import os
from app.log import logger
import psycopg2.extras
from datetime import datetime

class Database:
    def __init__(self):
        self.db = psycopg2.connect(
                    dbname=os.getenv('DB_NAME'),
                    user=os.getenv('DB_USER'),
                    password=os.getenv('DB_PASS'),
                    host=os.getenv('DB_HOST'),
                    port=os.getenv('DB_PORT')
                )
    
    def __execute_query(self, query, params=None, fetchone=False, fetchall=False):
        cur = self.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cur.execute(query, params)
            if fetchone:
                result = cur.fetchone()
            elif fetchall:
                result = cur.fetchall()
            else:
                result = None
            self.db.commit()
            return result
        except Exception as e:
            self.db.rollback()
            logger.error(f"Database Error: {e}")
            raise
        finally:
            cur.close()
       
    def initialize_database(self):
        query = """
                DROP TABLE IF EXISTS consultation_record CASCADE;
                DROP TABLE IF EXISTS doctor CASCADE;
                DROP TABLE IF EXISTS organization_user_map CASCADE;
                DROP TABLE IF EXISTS organization CASCADE;
                DROP TABLE IF EXISTS app_user CASCADE;

                CREATE TABLE IF NOT EXISTS app_user (
                    user_id VARCHAR(32) PRIMARY KEY,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    is_admin BOOLEAN DEFAULT FALSE,
                    phone_number VARCHAR(10) NOT NULL,
                    aadhaar_number VARCHAR(20),
                    dob DATE,
                    gender VARCHAR(10),
                    chronic_diseases TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS organization (
                    organization_id VARCHAR(32) PRIMARY KEY,
                    organization_name VARCHAR(100) NOT NULL,
                    license_number VARCHAR(50) UNIQUE NOT NULL,
                    address TEXT,
                    contact_number VARCHAR(15),
                    admin_id VARCHAR(32) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (admin_id) REFERENCES app_user(user_id)
                );

                CREATE TABLE IF NOT EXISTS organization_user_map (
                    id SERIAL PRIMARY KEY,
                    organization_id VARCHAR(32) NOT NULL,
                    user_id VARCHAR(32) NOT NULL,
                    role VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (organization_id) REFERENCES organization(organization_id),
                    FOREIGN KEY (user_id) REFERENCES app_user(user_id)
                );

                CREATE TABLE IF NOT EXISTS doctor (
                    doctor_id VARCHAR(32) PRIMARY KEY,
                    user_id VARCHAR(32) NOT NULL,
                    organization_id VARCHAR(32) NOT NULL,
                    specialization VARCHAR(100),
                    license_number VARCHAR(50) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES app_user(user_id),
                    FOREIGN KEY (organization_id) REFERENCES organization(organization_id)
                );

                CREATE TABLE IF NOT EXISTS consultation_record (
                    record_id VARCHAR(32) PRIMARY KEY,
                    patient_id VARCHAR(32) NOT NULL,
                    doctor_id VARCHAR(32) NOT NULL,
                    organization_id VARCHAR(32) NOT NULL,
                    transcript TEXT,
                    top_5_disease JSONB,
                    prescribed_medicine TEXT[],
                    transcript_summary TEXT,
                    consultation_date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (patient_id) REFERENCES app_user(user_id),
                    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id),
                    FOREIGN KEY (organization_id) REFERENCES organization(organization_id)
                );
            """
        return self.__execute_query(query)

    # User-related db calls
    def create_user(self, user_id, email, password_hash, name, is_admin, phone_number, aadhaar_number, dob, gender, chronic_diseases):
        query = """
            INSERT INTO app_user (user_id, email, password_hash, name, is_admin, phone_number, aadhaar_number, dob, gender, chronic_diseases)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING user_id;
        """
        return self.__execute_query(query, (user_id, email, password_hash, name, is_admin, phone_number, aadhaar_number, dob, gender, chronic_diseases), fetchone=True)['user_id']

    def get_user_by_email(self, email):
        query = "SELECT * FROM app_user WHERE email = %s"
        return self.__execute_query(query, (email,), fetchone=True)

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM app_user WHERE user_id = %s"
        return self.__execute_query(query, (user_id,), fetchone=True)

    def get_user_admin_privilage_by_id(self, user_id):
        query = "SELECT is_admin FROM app_user WHERE user_id = %s"
        return self.__execute_query(query, (user_id,), fetchone=True)
    
    def get_user_patient_data(self,email):
        query = "SELECT name, user_id, email, dob, phone_number, gender, chronic_diseases FROM app_user WHERE email = %s"
        return self.__execute_query(query, (email,), fetchone=True)

    def update_user_privilage(self, user_id, is_admin):
        query = "UPDATE app_user SET is_admin = %s, updated_at = %s WHERE user_id = %s"
        self.__execute_query(query, (is_admin, datetime.now(),user_id))

    #Doctor-related db calls
    def create_doctor(self, doctor_id, user_id, organization_id, specialization, license_number):
        query = """
            INSERT INTO doctor (doctor_id, user_id, organization_id, specialization, license_number)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING doctor_id;
        """
        return self.__execute_query(query, (doctor_id, user_id, organization_id, specialization, license_number), fetchone=True)['doctor_id']

    def get_doctor_by_user_id(self, user_id):
        query = "SELECT * FROM doctor WHERE user_id = %s"
        return self.__execute_query(query, (user_id,), fetchall=True)
    
    def get_doctor_organization(self, user_id):
        query = """
            SELECT o.organization_name, o.organization_id
            FROM doctor d
            JOIN organization o ON d.organization_id = o.organization_id
            WHERE d.user_id = %s;"""
        return self.__execute_query(query, (user_id,), fetchall=True)
    
    # Organization-related db calls
    def create_organization(self, organization_id, organization_name, license_number, address, contact_number, admin_id):
        query = """
            INSERT INTO organization (organization_id, organization_name, license_number, address, contact_number, admin_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING organization_id;
        """
        return self.__execute_query(query, (organization_id, organization_name, license_number, address, contact_number, admin_id), fetchone=True)['organization_id']
    
    def get_organization_by_license(self, license_number):
        query = "SELECT * FROM organization WHERE license_number = %s"
        return self.__execute_query(query, (license_number,), fetchone=True)


    # Consultation-related db calls
    def create_consultation_record(self, record_id, patient_id, doctor_id, organization_id):
        query = """
            INSERT INTO consultation_record (record_id, patient_id, doctor_id, organization_id)
            VALUES (%s, %s, %s, %s)
            RETURNING record_id;
        """
        return self.__execute_query(query, (record_id, patient_id, doctor_id, organization_id), fetchone=True)['record_id']
    
    def get_consultation_records(self, patient_id):
        query = """
            SELECT 
            u.name AS patient_name, 
            d.name AS doctor_name, 
            o.organization_name, 
            cr.top_5_disease, 
            cr.prescribed_medicine, 
            cr.transcript_summary, 
            cr.consultation_date_time
            FROM consultation_record cr
            JOIN app_user u ON cr.patient_id = u.user_id
            JOIN doctor doc ON cr.doctor_id = doc.doctor_id
            JOIN app_user d ON doc.user_id = d.user_id
            JOIN organization o ON cr.organization_id = o.organization_id
            WHERE cr.patient_id = %s
            ORDER BY cr.consultation_date_time DESC
        """
        return self.__execute_query(query, (patient_id,), fetchall=True)
    
    def update_consultation_record(self, record_id, transcript_summary, top_5_disease, prescribed_medicine):
        query = """
            UPDATE consultation_record
            SET transcript_summary = %s, top_5_disease = %s, prescribed_medicine = %s, updated_at = %s
            WHERE record_id = %s;
        """
        self.__execute_query(query, (transcript_summary, json.dumps(top_5_disease), prescribed_medicine, datetime.now(), record_id))
db = Database()