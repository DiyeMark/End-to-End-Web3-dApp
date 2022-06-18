from pymongo import MongoClient, ASCENDING
from pymongo.results import UpdateResult
from backend.models.Trainee import Trainee


class TraineeDb(object):
    def __init__(self, host, port=27017, user_name='', password='password', database='staff_db'):
        self.host = host
        self.port = port
        self.user_name = user_name
        self.password = password
        self.database = database
        self.client = MongoClient(host=self.host, port=self.port)
        self.db = self.client[self.database]
        self.db.users.create_index([("uuid", ASCENDING)], unique=True)
        self.collection = self.db.users

    def find_by_uuid(self, uuid):
        return self.collection.find_one({"uuid": uuid})

    def find(self, filter_dic):
        return self.collection.find_one(filter_dic)

    def insert(self, user: Trainee) -> Trainee:
        filter_dic = {'uuid': user.uuid}
        if not self.find(filter_dic):
            user.id = self.collection.insert_one(user.get_map_object()).inserted_id
            return user
        else:
            data = self.find(filter_dic)
            return Trainee.User.from_dict(data)

    def insert_or_update(self, user: Trainee) -> Trainee:
        filter_dic = {'uuid': user.uuid}
        if not self.find(filter_dic):
            user.id = self.collection.insert_one(user.get_map_object()).inserted_id
            user_data = self.find(filter_dic)
            return Trainee.User.from_dict(user_data)
        else:
            self.update(filter_dic, user.get_map_object())
            user_data = self.find(filter_dic)
            test = Trainee.User.from_dict(user_data)
            return test

    def update(self, filter_dic, update_data) -> UpdateResult:
        new_values = {"$set": update_data}
        return self.collection.update_one(filter_dic, new_values)

    def updates(self, filter_dic, update_data):
        new_values = {"$set": update_data}
        self.collection.update_many(filter_dic, new_values)

    def delete(self, filter_dic):
        self.collection.delete_one(filter_dic)

    def deletes(self, filter_dic):
        self.collection.delete_many(filter_dic)
