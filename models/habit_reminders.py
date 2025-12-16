import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma
from datetime import datetime

from db import db

class HabitReminders(db.Model):
    __tablename__="HabitReminders"

    reminder_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Users.user_id"), nullable=False)
    habit_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Habits.habit_id"), nullable=False)
    reminder_time = db.Column(db.String(), nullable=False, unique=True)
    repeat_days = db.Column(db.String())
    message = db.Column(db.String())
    created_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean(), default=True)

    user = db.relationship("Users", foreign_keys='[HabitReminders.user_id]', back_populates = 'habitReminders')
    habit = db.relationship("Habits", foreign_keys='[HabitReminders.habit_id]', back_populates = 'habitReminder')


    def __init__(self,user_id,habit_id,reminder_time, repeat_days, message,created_date,is_active=True):
        self.user_id=user_id
        self.habit_id=habit_id
        self.reminder_time=reminder_time
        self.repeat_days=repeat_days
        self.message=message
        self.created_date=created_date
        self.is_active=is_active

    def new_habitReminder_obj():
        return HabitReminders('','','','','',datetime.now(),True)

class HabitRemindersSchema(ma.Schema):
    class Meta:
        fields = ['reminder_id', 'reminder_time', 'repeat_days', 'message', 'created_date', 'is_active', 'user', 'habit']

    reminder_id= ma.fields.UUID()
    reminder_time=ma.fields.String(required=True)
    repeat_days = ma.fields.String(allow_none=True)
    message = ma.fields.String(allow_none=True)
    created_date=ma.fields.DateTime(required=True)
    is_active=ma.fields.Boolean(allow_none=True, dump_default=True)

    user = ma.fields.Nested("UsersSchema")
    habit = ma.fields.Nested("HabitsSchema")

habitReminder_schema=HabitRemindersSchema()
habitReminders_schema=HabitRemindersSchema(many=True)


