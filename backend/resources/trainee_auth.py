from flask import request
from backend.models.Trainee import Trainee
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


class TraineeSignupApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            print(body)
            trainee = Trainee(**body)
            trainee.hash_password()
            trainee.save()
            id = trainee.id
            return {'id': str(id)}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            raise EmailAlreadyExistsError
        except Exception:
            raise InternalServerError


class TraineeLoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            trainee = Trainee.objects.get(email=body.get('email'))
            authorized = trainee.check_password(body.get('password'))
            if not authorized:
                return {'error': 'Email or password invalid'}, 401

            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(trainee.id), expires_delta=expires)
            # return {'token': access_token.decode('utf-8')}, 200
            return {'token': access_token}, 200

        except(UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception:
            raise InternalServerError
