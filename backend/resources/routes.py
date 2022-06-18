
from .staff_auth import StaffSignupApi, StaffLoginApi
from .trainee_auth import TraineeSignupApi, TraineeLoginApi
from .trainee import TraineesApi, TraineeApi


def initialize_routes(api):
    # staff routes
    api.add_resource(StaffSignupApi, '/api/auth/staff/signup')
    api.add_resource(StaffLoginApi, '/api/auth/staff/login')

    api.add_resource(TraineesApi, '/api/trainee')
    api.add_resource(TraineeApi, '/api/trainee/<_id>')

    # trainee routes
    api.add_resource(TraineeSignupApi, '/api/auth/trainee/signup')
    api.add_resource(TraineeLoginApi, '/api/auth/trainee/login')
