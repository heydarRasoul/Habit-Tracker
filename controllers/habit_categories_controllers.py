from flask import request, jsonify

from db import db
from models.habit_categories import HabitCategories, habitCategories_schema, habitCategory_schema
from util.reflection import populate_obj
from lib.authentication import authenticate_return_auth, authenticate

@authenticate
def add_category():
    post_data = request.form if request.form else request.json

    new_category= HabitCategories.new_habitCategory_obj()
    populate_obj(new_category, post_data)

    try:
        db.session.add(new_category)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"messsage":"unable to create category"}),400
    
    return jsonify({"message":"category created", "result": habitCategory_schema.dump(new_category)}),201


@authenticate
def get_all_habitCategories():
    query= db.session.query(HabitCategories).all()

    if not query:
        return jsonify({"message":"no category found"}), 400
    else:
        return jsonify({"message":"categories found", "results": habitCategories_schema.dump(query)}),200



@authenticate
def get_habitCategory_by_id(category_id):
    query = db.session.query(HabitCategories).filter(HabitCategories.category_id == category_id ).first()

    if not query:
        return jsonify({"message": "no category with provided id founded."})
    else:
        return jsonify({"message": "category found", "result": habitCategory_schema.dump(query)}),200
    


@authenticate_return_auth
def update_category_by_id(category_id, auth_info):
    query = db.session.query(HabitCategories).filter(HabitCategories.category_id == category_id).first()
    post_data = request.form if request.form else request.get_json()
    if not query:
        return jsonify({"message":"category not found"}), 404

    if auth_info.user.role == 'admin':
        populate_obj(query, post_data)
        db.session.commit()
   
        return jsonify({"message": "company found", "results": habitCategory_schema.dump(query)}), 200
    
    return jsonify({"message":"unathorized"}),400



@authenticate_return_auth
def delete_category_by_id(category_id, auth_info):
    query = db.session.query(HabitCategories).filter(HabitCategories.category_id == category_id).first()
    if not query:
        return jsonify({"message":"category not found"}), 404

    if auth_info.user.role == 'admin':

        db.session.delete(query)
        db.session.commit()

        return jsonify({"message":"category deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
        
    