from db import db

class UserModel(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(255))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @classmethod
    def get_user(cls, username):
        return cls.query.filter_by(username = username).first()