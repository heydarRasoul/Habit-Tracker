import marshmallow as ma 
import uuid
from sqlalchemy.dialects.postgresql import UUID 

from db import db

class Profiles(db.Model):
    __tablename__="Profiles"

    profile_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Profiles.user_id"), nullable=False)
    first_name = db.Column(db.String(),nullable=False)
    last_name = db.Column(db.String())
    dob = db.Column(db.String())
    bio = db.Column(db.String())

    user = db.relationship("Users", foreign_keys='[Profiles.user_id]', back_populates = 'profile')

    def __init__(self,user_id,first_name, last_name, dob, bio):
        self.user_id=user_id
        self.first_name=first_name
        self.last_name=last_name
        self.dob=dob
        self.bio=bio


    def new_profile_obj():
        return Profiles('','','','','')
    

class ProfilesSchema(ma.Schema):
    class Meta:
        fields = ['profile_id','first_name','last_name','dob','bio','user']

    profile_id = ma.fields.UUID()
    first_name = ma.fiels.String(required=True)
    last_name = ma.fields.String(allow_none=True)
    dob = ma.fields.String(allow_none=True)
    bio = ma.fields.String(allow_none=True)

    user = ma.fields.Nested("UsersSchema")


profile_schema = ProfilesSchema()
