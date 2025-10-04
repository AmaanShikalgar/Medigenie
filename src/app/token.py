import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()

from .log import logger
from .message import IS_SUCCESS, IS_ERROR, STATUS

class Token:
    def __init__(self):
        pass

    def generate_token(self,user_id):
        try:
            token = jwt.encode({
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }, os.getenv('AUTH_SECRET_KEY'), algorithm='HS256')
            return token
        except Exception as e:
            logger.error(f"Token Generation Error: {e}")
            return None
        
    def isTokenValid(self,token):
        try:
            decoded = jwt.decode(token, os.getenv('AUTH_SECRET_KEY'), algorithms=['HS256'])
            if 'exp' in decoded and datetime.utcnow() > datetime.fromtimestamp(decoded['exp']):
                resp = IS_ERROR["ERR_AUTH_TOKEN_EXPIRED"]
                status = STATUS["BAD_REQUEST"]
                logger.error("Token has expired")
                return resp, status
            resp = IS_SUCCESS['AUTH_TOKEN_VALID']
            status = STATUS["OK"]
            return resp, status
        except jwt.ExpiredSignatureError as e:
            resp = IS_ERROR["ERR_AUTH_TOKEN_EXPIRED"]
            status = STATUS["BAD_REQUEST"]
            logger.error(f"Token has expired. Error - {e}")
            return resp, status
        except jwt.InvalidTokenError as e:
            resp = IS_ERROR["ERR_AUTH_TOKEN_INVALID"]
            status = STATUS["BAD_REQUEST"]
            logger.error(f"Invalid token. Error - {e}")
            return resp, status
        except Exception as e:
            resp = IS_ERROR["ERR_AUTH_TOKEN_INVALID"]
            status = STATUS["BAD_REQUEST"]
            logger.error(f"Token Validation Error: {e}")
            return resp, status
        
token_obj = Token()