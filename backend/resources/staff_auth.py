from flask import request

from backend.helpers.AccountHelper import generate_algorand_keypair
from backend.models.Staff import Staff
from flask_restful import Resource
from flask_jwt_extended import create_access_token
import datetime
from mongoengine.errors import (FieldDoesNotExist,
                                NotUniqueError,
                                DoesNotExist)
from backend.resources.error import (InternalServerError,
                                    SchemaValidationError,
                                    EmailAlreadyExistsError,
                                    UnauthorizedError)


class StaffSignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            print(body)
            admin = Staff(**body)
            admin.hash_password()
            admin.generate_algorand_keypair()
            admin.save()
            id = admin.id
            return {'id': str(id)}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception:
            raise InternalServerError


class StaffLoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            admin = Staff.objects.get(email=body.get('email'))
            authorized = admin.check_password(body.get('password'))
            if not authorized:
                return {'error': 'Email or password invalid'}, 401

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(admin.id), expires_delta=expires)
            # return {'token': access_token.decode('utf-8')}, 200
            return {'token': access_token}, 200

        except(UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception:
            raise InternalServerError
