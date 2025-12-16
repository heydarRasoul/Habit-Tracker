import uuid 
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma 
from datetime import datetime

from db import db 
from .users_challenge_xref import user_challenge_xref

class HabitChallenges(db.Model):
    __tablename__="HabitChallenges"

    challenge_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    challenge_name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String())
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.String())
    created_date = db.Column(db.DateTime)

   
    users = db.relationship("Users", secondary=user_challenge_xref, back_populates='challenges')

    def __init__(self, user_id, challenge_name, description, start_date, end_date, created_date):
        self.user_id=user_id
        self.challenge_name=challenge_name
        self.description=description
        self.start_date=start_date
        self.end_date=end_date
        self.created_date=created_date

    
    def new_habitChallenge_obj():
        return HabitChallenges('','','','','',datetime.now())
    

class HabitChallengesSchema(ma.Schema):
    class Meta:
        fields = ['challenge_id','challenge_name','description','start_date','end_date','created_date','user']

    challenge_id=ma.fields.UUID()
    challenge_name=ma.fields.String(required=True)
    description=ma.fields.String(allow_none=True)
    start_date=ma.fields.DateTime(required=True)
    end_date=ma.fields.String(allow_none=True)
    created_date=ma.fields.DateTime(required=True)

    user = ma.fields.Nested("UsersSchema",  many=True, exclude=['challenges'])

habitChallenge_schema=HabitChallengesSchema()
habitChallenges_schema=HabitChallengesSchema(many=True)
