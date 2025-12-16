import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db
from .habit_category_xref import habit_category_xref

class HabitCategories(db.Model):
    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String())


    habits = db.relationship("Habits", secondary=habit_category_xref, back_populates='categories')



    def __init__(self,category_name,description):
        self.category_name=category_name
        self.description=description
    

    def new_habitCategory_obj():
        return HabitCategories('','')


class HabitCategoriesSchema(ma.Schema):
    class Meta:
        fields = ['category_id', 'category_name', 'description', 'habits']

    category_id= ma.fields.UUID()
    category_name=ma.fields.String(required=True)
    description = ma.fields.String(allow_none=True)
   
    user = ma.fields.Nested("UsersSchema")
    habits = ma.fields.Nested("HabitsSchema", many=True, exclude=['categories'])

habitCategory_schema=HabitCategoriesSchema()
habitCategories_schema=HabitCategoriesSchema(many=True)