IS_SUCCESS = {
    "DATABASE_INITIALIZED": {"code": "db_init", "message": "Database initialized successfully"},
    "LOGIN_SUCCESS": {"code": "login_success", "message": "Login successful"},
    "REGISTRATION_SUCCESS": {"code": "registration_success", "message": "Registration successful"},
    "ANALYZE_SUCCESS": {"code": "analyze_success", "message": "Transcript analysis successful"},

    # User-related success messages
    "USER_CREATED": {"code": "user_created", "message": "User created successfully"},
    "USER_UPDATED": {"code": "user_updated", "message": "User updated successfully"},
    "USER_FOUND": {"code": "user_found", "message": "User found"},

    # Organization-related success messages
    "ORG_FOUND": {"code": "org_found", "message": "Organization found"},

    # Token-related success messages
    "AUTH_TOKEN_VALID": {"code": "auth_token_valid", "message": "Authentication token is valid"},

    # Consultation-related success messages
    "CONSULTATION_CREATED": {"code": "consultation_created", "message": "Consultation record created successfully"},
    "CONSULTATION_FOUND": {"code": "consultation_found", "message": "Consultation record found"},

    "TRANSCRIPTION_SUCCESS": {"code": "transcription_success", "message": "Transcription completed successfully"},
}

IS_ERROR = {
    "ERR_DATABASE_INITIALIZATION": {"code": "db_init", "message": "Database initialization failed"},
    "ERR_TRANSCRIPT_MISSING":{ "code": "transcript_missing", "message": "Transcript is missing in the request"},
    "ERR_ANALYZE_FAILED":{ "code": "analyze_failed", "message": "Transcript analysis failed"},

    # User-related errors
    "ERR_USER_NOT_FOUND": {"code": "user_not_found", "message": "User not found"},
    "ERR_USER_INVALID_CREDENTIALS": {"code": "invalid_credentials", "message": "Invalid credentials"},
    "ERR_USER_LOGIN_FAILED": {"code": "login_failed", "message": "Login failed"},
    "ERR_USER_ALREADY_EXISTS": {"code": "user_already_exists", "message": "User already exists"},
    "ERR_USER_CREATION_FAILED": {"code": "user_creation_failed", "message": "User creation failed"},
    "ERR_USER_ID_MISSING": {"code": "user_id_missing", "message": "User ID is missing"},
    "ERR_USER_MAIL_MISSING": {"code": "user_mail_missing", "message": "User email is missing"},
    "ERR_USER_UNAUTHORIZED": {"code": "user_unauthorized", "message": "User is not authorized to perform this action"},
    "ERR_USER_PRIVILEGE_MISSING": {"code": "user_privilege_missing", "message": "User privilege is missing"},
    "ERR_USER_UPDATE_FAILED": {"code": "user_update_failed", "message": "User update failed"},
    "ERR_USER_GET_FAILED": {"code": "user_get_failed", "message": "User retrieval failed"},

    # Admin-related errors
    "ERR_ADMIN_NOT_FOUND": {"code": "admin_not_found", "message": "Admin email not found"},
    "ERR_ADMIN_ORG_DUPLICATE": {"code": "admin_org_duplicate", "message": "Cannot create multiple organizations with the same Email ID"},

    # Doctor-related errors
    "ERR_DOCTOR_ID_MISSING": {"code": "doctor_id_missing", "message": "Doctor ID is missing in the request"},

    # Token-related errors
    "ERR_AUTH_TOKEN_MISSING": {"code": "auth_token_missing", "message": "Authentication token is missing"},
    "ERR_AUTH_TOKEN_INVALID": {"code": "auth_token_invalid", "message": "Invalid authentication token"},
    "ERR_AUTH_TOKEN_EXPIRED": {"code": "auth_token_expired", "message": "Authentication token has expired"},

    #Organization related errors
    "ERR_ORG_ALREADY_EXISTS": {"code": "org_already_exists", "message": "Organization already exists"},
    "ERR_ORG_NOT_FOUND": {"code": "org_not_found", "message": "Organization not found"},
    "ERR_ORG_CREATION_FAILED": {"code": "org_creation_failed", "message": "Organization creation failed"},

    # Consultation-related errors
    "ERR_CONS_CREATE_FAILED": {"code": "consultation_create_failed", "message": "Consultation record creation failed"},
    "ERR_CONS_NOT_FOUND": {"code": "consultation_not_found", "message": "Consultation record not found"},
    "ERR_CONS_GET_FAILED": {"code": "consultation_get_failed", "message": "Consultation retrieval failed"},

    "ERR_AUDIO_FILE_SAVE_FAILED": {"code": "audio_file_save_failed", "message": "Failed to save the audio file"},
}


STATUS = {
    "INTERNAL_SERVER_ERROR": 500,
    "BAD_REQUEST": 400,
    "NOT_FOUND": 404,
    "OK": 200,
}