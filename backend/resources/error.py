class InternalServerError(Exception):
    pass


class SchemaValidationError(Exception):
    pass


class TraineeAlreadyExistsError(Exception):
    pass


class TraineeNotExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class EmailDoesNotExistsError(Exception):
    pass


class BadTokenError(Exception):
    pass


class ExpiredTokenError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


errors = {
    "InternalServerError": {
        "message": "Something went wrong",
        "status": 500
    },
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400
    },
    "TraineeAlreadyExistsError": {
        "message": "Category with given name already exists",
        "status": 400
    },
    "TraineeNotExistsError": {
        "message": "Category with given id doesn't exists",
        "status": 400
    },
    "EmailAlreadyExistsError": {
        "message": "User with given email address already exists",
        "status": 400
    },
    "UnauthorizedError": {
        "message": "Invalid username or password",
        "status": 401
    },
    "EmailDoesNotExistsError": {
        "message": "Couldn't find the user with given email address",
        "status": 400
    },
    "BadTokenError": {
        "message": "Invalid token",
        "status": 403
    },
    "ExpiredTokenError": {
        "message": "Expired token",
        "status": 403
    }
}
