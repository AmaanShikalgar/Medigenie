from flask import Blueprint, render_template, jsonify, request
import psycopg2
med_bp = Blueprint('med', __name__)

from app.database import db
from app.message import IS_SUCCESS, IS_ERROR, STATUS
from app.log import logger
from app.redis import cache
from app.user import User
from app.doctor import Doctor
from app.organization import Organization
from app.token import token_obj
from app.decorator import token_required, admin_required, sudo_admin_required
from app.consultation import Consultation
from app.transcriber import Transcriber

@med_bp.route('/')
def hello():
    return render_template('index.html')


@med_bp.route('/init-db',methods=['POST'])
def init_db():
    try:
        db.initialize_database()
        resp = IS_SUCCESS["DATABASE_INITIALIZED"]
        status = STATUS["OK"]

    except Exception as e:
        logger.error(f"Database Error: {e}")
        resp = IS_ERROR["ERR_DATABASE_INITIALIZATION"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
    
    return jsonify(resp), status

@med_bp.route('/login',methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            resp = IS_ERROR["ERR_USER_INVALID_CREDENTIALS"]
            status = STATUS["BAD_REQUEST"]

        user = User(email=email, password=password)
        valid, user_id, doctor_id = user.isUserValid()
        if not valid:
            resp = IS_ERROR["ERR_USER_NOT_FOUND"]
            status = STATUS["NOT_FOUND"]
        else:
            token = token_obj.generate_token(user_id)
            resp = IS_SUCCESS["LOGIN_SUCCESS"]
            status = STATUS["OK"]
            resp['user_id'] = user_id
            resp['token'] = token
            if doctor_id:
                resp['doctor_id'] = doctor_id

    except Exception as e:
        logger.error(f"Login Error: {e}")
        resp = IS_ERROR["ERR_USER_LOGIN_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
    
    return jsonify(resp), status

@med_bp.route('/create', methods=['POST'])
def create():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        phone_number = data.get('phone_number')
        aadhaar_number = data.get('aadhaar_number')
        dob = data.get('dob')
        gender = data.get('gender')
        chronic_diseases = data.get('chronic_diseases')
        user = User(
            email=email,
            password=password,
            name=name,
            phone_number=phone_number,
            adhaar_number=aadhaar_number,
            dob=dob,
            gender=gender,
            chronic_diseases=chronic_diseases
        )
        created, user_id = user.create()
        if not created:
            resp = IS_ERROR["ERR_USER_ALREADY_EXISTS"]
            status = STATUS["BAD_REQUEST"]
        else:
            resp = IS_SUCCESS["USER_CREATED"]
            status = STATUS["OK"]
            resp['user_id'] = user_id

    except Exception as e:
        logger.error(f"Registration Error: {e}")
        resp = IS_ERROR["ERR_USER_CREATION_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status

@med_bp.route('/create-organization',methods=['POST'])
@admin_required
def create_organization():
    try:
        data = request.get_json()
        org_name = data.get("organization_name")
        license_number = data.get("license_number")
        address = data.get("address")
        contact_number = data.get("contact_number")
        admin_email = data.get("admin_email")
        user = User(email=admin_email,password=None)
        user_exits, admin_id = user.get_user_id_by_email()
        if not user_exits:
            resp = IS_ERROR["ERR_ADMIN_NOT_FOUND"]
            status = STATUS["BAD_REQUEST"]
        else:
            organization = Organization(
                name=org_name,
                license_number=license_number,
                address=address,
                contact_number=contact_number,
                admin_id=admin_id
            )
            created, organization_id = organization.create()
            if not created:
                resp = IS_ERROR["ERR_ORG_ALREADY_EXISTS"]
                status = STATUS["BAD_REQUEST"]
            else:
                resp = IS_SUCCESS["REGISTRATION_SUCCESS"]
                status = STATUS["OK"]
                resp["organization_id"] = organization_id

    except psycopg2.errors.UniqueViolation as e:
        logger.error(f"Unique Violation Error: {e}")
        resp = IS_ERROR["ERR_ADMIN_ORG_DUPLICATE"]
        status = STATUS["BAD_REQUEST"]
    except Exception as e:
        logger.error(f"Oragnization Registration Error: {e}")
        resp = IS_ERROR["ERR_ORG_CREATION_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status

@med_bp.route('/update-user-privilege',methods=['POST'])
@sudo_admin_required
def update_user_privilege():
    try:
        data = request.get_json()
        user_email = data.get('user_email')
        is_admin = data.get("is_admin")
        if user_email is None:
            resp = IS_ERROR["ERR_USER_MAIL_MISSING"]
            status = STATUS["BAD_REQUEST"]
        elif is_admin is None:
            resp = IS_ERROR["ERR_USER_PRIVILEGE_MISSING"]
            status = STATUS["BAD_REQUEST"]
        user = User(email=user_email,password=None)
        user_exits, user_id = user.get_user_id_by_email()
        if not user_exits:
            resp = IS_ERROR["ERR_USER_NOT_FOUND"]
            status = STATUS["BAD_REQUEST"]
        else:
            db.update_user_privilage(user_id,is_admin)
            resp = IS_SUCCESS["USER_UPDATED"]
            status = STATUS["OK"]

    except Exception as e:
        logger.error(f"Update User Privilege Error: {e}")
        resp = IS_ERROR["ERR_USER_UPDATE_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status

@med_bp.route('/register-doctor',methods=['POST'])
def register_doctor():
    try:
        data = request.get_json()
        doctor_mail = data.get('doctor_mail')
        organization_id = data.get('organization_id')
        specialization = data.get('specialization')
        license_number = data.get('license_number')
        user = User(email=doctor_mail,password=None)
        user_exits, user_id = user.get_user_id_by_email()
        if not user_exits:
            resp = IS_ERROR["ERR_USER_NOT_FOUND"]
            status = STATUS["BAD_REQUEST"]
        else:
            doctor = Doctor(
                user_id=user_id,
                organization_id=organization_id,
                specialization=specialization,
                license_number=license_number
            )
            doctor_registered, doctor_id = doctor.register()
            if not doctor_registered:
                resp = IS_ERROR["ERR_USER_ALREADY_EXISTS"]
                status = STATUS["BAD_REQUEST"]
            else:
                resp = IS_SUCCESS["REGISTRATION_SUCCESS"]
                status = STATUS["OK"]
                resp['doctor_id'] = doctor_id
                resp['user_id'] = user_id
    except Exception as e:
        logger.error(f"Doctor Registration Error: {e}")
        resp = IS_ERROR["ERR_REGISTRATION_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status

@med_bp.route('/get-doctor-organization',methods=['GET'])
def get_doctor_organization():
    try:
        user_id = request.headers.get('UserID')
        if user_id is None:
            resp = IS_ERROR["ERR_USER_ID_MISSING"]
            status = STATUS["BAD_REQUEST"]
        else:
            doctor = Doctor(user_id=user_id)
            organization = doctor.get_doctor_organization_by_user_id()
            if not organization:
                resp = IS_ERROR["ERR_ORG_NOT_FOUND"]
                status = STATUS["NOT_FOUND"]
            else:
                resp = IS_SUCCESS["ORG_FOUND"]
                status = STATUS["OK"]
                resp['organization'] = organization
    except Exception as e:
        logger.error(f"Get Doctor Organization Error: {e}")
        resp = IS_ERROR["ERR_ORG_NOT_FOUND"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status

@med_bp.route('/get-patient-data',methods=['POST'])
def get_user():
    try:
        data = request.get_json()
        user_email = data.get('user_email')
        if user_email is None:
            resp = IS_ERROR["ERR_USER_ID_MISSING"]
            status = STATUS["BAD_REQUEST"]
        else:
            patient = User(email=user_email)
            patient_data = patient.get_user_patient_data()
            if not patient_data:
                resp = IS_ERROR["ERR_USER_NOT_FOUND"]
                status = STATUS["NOT_FOUND"]
            else:
                resp = IS_SUCCESS["USER_FOUND"]
                status = STATUS["OK"]
                resp['patient'] = patient_data
    except Exception as e:
        logger.error(f"Get User Error: {e}")
        resp = IS_ERROR["ERR_USER_GET_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status

@med_bp.route('/create-consultation',methods=['POST'])
def create_consultation():
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        organization_id = data.get('organization_id')
        if not patient_id or not doctor_id or not organization_id:
            resp = IS_ERROR["ERR_USER_ID_MISSING"]
            status = STATUS["BAD_REQUEST"]
        else:
            consultation_record = Consultation(patient_id=patient_id, doctor_id=doctor_id, organization_id=organization_id)
            record_id = consultation_record.create()
            resp = IS_SUCCESS["CONSULTATION_CREATED"]
            status = STATUS["OK"]
            resp['record_id'] = record_id
    except Exception as e:
        logger.error(f"Analyze Error: {e}")
        resp = IS_ERROR["ERR_CONS_CREATE_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
    
    return jsonify(resp), status

@med_bp.route('/get-previous-consultation', methods=['POST'])
def get_previous_consultation():
    try:
        patient_id = request.get_json().get('patient_id')
        if not patient_id:
            resp = IS_ERROR["ERR_USER_ID_MISSING"]
            status = STATUS["BAD_REQUEST"]
        else:
            consultation = Consultation(patient_id=patient_id)
            records = consultation.get_previous_consultation_records()
            if not records:
                resp = IS_ERROR["ERR_CONS_NOT_FOUND"]
                status = STATUS["NOT_FOUND"]
            else:
                resp = IS_SUCCESS["CONSULTATION_FOUND"]
                status = STATUS["OK"]
                resp['records'] = records
    except Exception as e:
        logger.error(f"Get Previous Consultation Error: {e}")
        resp = IS_ERROR["ERR_CONS_GET_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]

    return jsonify(resp), status

@med_bp.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        record_id = data.get('consultation_id')
        transcript = data.get('transcript')
        if not transcript:
            resp = IS_ERROR["ERR_TRANSCRIPT_MISSING"]
            status = STATUS["BAD_REQUEST"]
        else:
            consultation_obj = Consultation(record_id=record_id, transcript=transcript)
            consultation_obj.analyze_transcript()
            resp = IS_SUCCESS["ANALYZE_SUCCESS"]
            status = STATUS["OK"]
            resp['top_5_disease'] = consultation_obj.top_5_disease
            resp['prescribed_medicine'] = consultation_obj.prescribed_medicine
            resp['transcript_summary'] = consultation_obj.transcript_summary
    except Exception as e:
        logger.error(f"Analyze Error: {e}")
        resp = IS_ERROR["ERR_ANALYZE_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
    
    return jsonify(resp), status

@med_bp.route('/get-transcript',methods=['POST'])
def analyze_transcript():
    try:
        audio_file = request.files.get('audio_data')
        file_type = request.form.get('file_type','mp3')
        trans = Transcriber(model_name="turbo")
        file_path, audio_id = trans.save_audio_file(audio_file=audio_file, file_type=file_type)
        resp = IS_SUCCESS["TRANSCRIPTION_SUCCESS"]
        resp['transcript'] = trans.get_transcription(file_path)
        status = STATUS["OK"]
    except Exception as e:
        logger.error(f"Audio File Save Error: {e}")
        resp = IS_ERROR["ERR_AUDIO_FILE_SAVE_FAILED"]
        status = STATUS["INTERNAL_SERVER_ERROR"]
        
    return jsonify(resp), status