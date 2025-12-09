import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(), nallable=False, unique=True)
    email = db.Column(db.String(), nallable=False, unique=True)
    phone = db.Column(db.String())
    password = db.Column(db.String(), nallable=False)
    created_date = db.Column(db.DateTime)
    role = db.Column(db.String(), nallable=False, default="basic_user")
    is_active = db.Column(db.Boolean(), default=True)

    auth = db.relationship("AuthTokens",back_populates="user")
    profile = db.relationship("Profiles", foreign_keys='[Profiles.user_id]', back_populates='user', cascade="all")
    habit_challenges = db.relationship("HabitChallenges", foreign_keys='[HabitChallenges.user_id]', cascade="all")
    habits = db.relationship("Habits", foreign_keys='[Habits.user_id]', cascade="all")
    habitReminders = db.relationship("HabitReminders", foreign_keys='[HabitReminders.user_id]', cascade="all")

    def __init__(self, username, email, phone, password, created_date, role="basic_user", is_active=True):
        self.username=username
        self.email=email
        self.phone=phone
        self.passeord=password
        self.created_date=created_date
        self.role=role
        self.is_active=is_active

    def new_user_obj():
        return Users('','','','','','basic_user',True)  


class UsersSchema(ma.Schema):
    class Mete:
        fields = ['use-id','username', 'email', 'phone', 'created_date', 'role', 'is_active']   

    user_id=ma.fields.UUID()
    username=ma.fields.String(required=True)
    email=ma.fields.String(required=True)  
    phone=ma.fields.String()  
    created_date=ma.fields.DateTime(required=True)  
    role=ma.fields.String(required=True, dump_default='basic_user')
    is_active=ma.fields.Boolean(allow_none=True, dump_default=True)

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)