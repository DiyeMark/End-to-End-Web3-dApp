from flask import Response, request, jsonify, make_response
from backend.models import Trainee
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from mongoengine.errors import (FieldDoesNotExist,
                                NotUniqueError,
                                DoesNotExist,
                                ValidationError,
                                InvalidQueryError)
from backend.resources.error import (InternalServerError,
                                    SchemaValidationError,
                                    TraineeAlreadyExistsError,
                                    TraineeNotExistsError)


class TraineesApi(Resource):
    @jwt_required()
    def get(self):
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
        trainees = Trainee.objects.paginate(page=page, per_page=limit)

        return make_response(jsonify([trainee for trainee in trainees.items]), 200)

    @jwt_required()
    def post(self):
        try:
            body = request.get_json()
            trainee = Trainee(**body)
            trainee.save()
            return {'id': str(trainee.id)}, 200

        except (FieldDoesNotExist, ValidationError):
            raise SchemaValidationError

        except NotUniqueError:
            raise TraineeAlreadyExistsError
        except Exception:
            raise InternalServerError


class TraineeApi(Resource):

    @jwt_required()
    def get(self, _id):
        try:
            trainee = Trainee.objects.get(id=_id).to_json()
            return Response(trainee, mimetype="application/json", status=200)
            # category = Category.objects(id=id).first()
            # return make_response(jsonify(category), 200)
        except DoesNotExist:
            raise TraineeNotExistsError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def put(self, _id):
        try:
            body = request.get_json()
            trainee = Trainee.objects.get(id=_id)
            trainee.update(**body)

            return {'id': str(trainee.id)}, 200
        except InvalidQueryError:
            raise SchemaValidationError
        except DoesNotExist:
            raise TraineeNotExistsError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def delete(self, _id):
        try:
            trainee = Trainee.objects.get(id=_id)
            trainee.delete()
            # Category.objects.get(id=_id).delete()
            # return 'id: str(_id)', 200
            return {'id': str(trainee.id)}, 200
        except DoesNotExist:
            raise TraineeNotExistsError
        except Exception:
            raise InternalServerError
