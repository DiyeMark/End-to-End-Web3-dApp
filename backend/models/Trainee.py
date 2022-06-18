from backend.databases.db import db
from flask_bcrypt import generate_password_hash, check_password_hash


class Trainee(db.Document):
    username = db.StringField(required=True, unique=False)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True, min_length=6)
    public_key = db.StringField(required=True)
    private_key = db.StringField(required=True)
    passphrase_key = db.StringField(required=True)
    is_certificate_issued = db.BooleanField(required=True, default=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
