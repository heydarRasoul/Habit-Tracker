import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db

class HabitTracking(db.Model):
    __tablename__="HabitTracking"

    track_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    habit_id = db.Column(UUID(as_uuid=True), db.ForeignKey("HabitTracking.habit_id"), nullable=False)
    status = db.Column(db.String(), nullable=False)
    note = db.Column(db.String())
    units_completed = db.column(db.String())
   

    habit = db.relationship("Habits", foreign_keys='[HabitTracking.habit_id]', back_populates = 'habit_tracking')


    def __init__(self,habit_id,status,note, units_completed):
        self.habit_id=habit_id
        self.status=status
        self.note=note
        self.units_completed=units_completed
      

    def new_habit_obj():
        return HabitTracking('','','','')
    

class HabitTrackingSchema(ma.Schema):
    class Meta:
        fields = ['track_id', 'status', 'note', 'units_completed', 'habit']

    track_id= ma.fields.UUID()
    status=ma.fields.Strings(required=True)
    note = ma.fields.String(allow_none=True)
    units_completed = ma.fields.String(allow_none=True)
   
    habit = ma.fields.Nested("HabitsSchema")

HabitTracking_Schema=HabitTrackingSchema()
