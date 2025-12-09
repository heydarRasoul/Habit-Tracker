import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .habit_category_xref import habit_category_xref

class Habits(db.Model):
    __tablename__="Habits"

    habit_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("Habits.user_id"), nullable=False)
    title = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String())
    frequency_per_week = db.column(db.Integer())
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.String())
    is_active = db.Column(db.Boolean(), default=True)


    user = db.relationship("Users", foreign_keys='[Habits.user_id]', back_populates = 'habits')
    habitReminder = db.relationship("HabitReminders", foreign_keys='[HabitReminders.habit_id]', cascade="all")
    categories = db.relationship("Categories", secondary=habit_category_xref, back_populates='habits')
    habit_traking = db.relationship("HabitTracking", foreign_keys='[HabitTracking.habit_id]', cascade="all")



    def __init__(self,user_id,title,description, frequency_per_week, start_date,end_date,is_active=True):
        self.user_id=user_id
        self.title=title
        self.description=description
        self.frequency_per_week=frequency_per_week
        self.start_date=start_date
        self.end_date=end_date
        self.is_active=is_active

    def new_habit_obj():
        return Habits('','','',0,'','',True)

class HabitsSchema(ma.Schema):
    class Meta:
        fields = ['habit_id', 'title', 'description', 'frequency_per_weel', 'start_date', 'end_date', 'is_active', 'user','categories']

    habit_id= ma.fields.UUID()
    title=ma.fields.Strings(required=True)
    description = ma.fields.String(allow_none=True)
    frequency_per_week = ma.fields.Integer(allow_none=True)
    start_date=ma.fields.DateTime(required=True)
    end_date=ma.fields.String(allow_none=True)
    is_active=ma.fields.Boolean(allow_none=True, dump_default=True)

    user = ma.fields.Nested("UsersSchema")
    categories = ma.fields.Nested("HabitCategoriesSchema", many=True, exclude=['habits'])

habit_schema=HabitsSchema()
habits_schema=HabitsSchema(many=True)



