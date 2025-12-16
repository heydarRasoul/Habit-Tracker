from flask import request, jsonify

from db import db
from models.habits import Habits, habit_schema, habits_schema
from models.habit_categories import HabitCategories
from util.reflection import populate_obj
from lib.authentication import authenticate_return_auth, authenticate


@authenticate_return_auth
def add_habit(auth_info):
    post_data = request.form if request.form else request.json
    user_id = post_data.get('user_id')
    if str(auth_info.user_id) == user_id:

        new_habit = Habits.new_habit_obj()
        populate_obj(new_habit, post_data)

        try:
            db.session.add(new_habit)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message":"unable to add record."}), 400
        
        return jsonify({"message":"habit added","result": habit_schema.dump(new_habit)}), 201
    
    return jsonify({"message":"unathorized"}),401




@authenticate
def get_all_habits():
    
    habit_query = db.session.query(Habits).all()
   
    if not habit_query:
        return jsonify({"message": "users not founded."}),400

    return jsonify({"message":"users found", "results":habits_schema.dump(habit_query)}),200

    



@authenticate_return_auth
def get_habit_by_id(habit_id, auth_info):
    habit_query = db.session.query(Habits).filter(Habits.habit_id == habit_id).first()
    user_id = habit_query.user_id
    if not habit_query:
        return jsonify({"message":"habit not found"}), 404
    
    if auth_info.user_id == user_id:
        return jsonify({"message":"habit found", "result": habit_schema.dump(habit_query)}), 200

    return  jsonify({"message":"unathorized"}),400



@authenticate_return_auth
def add_habit_to_category(auth_info):
    post_data = request.form if request.form else request.json
    
    habit_id = post_data.get("habit_id")
    category_id = post_data.get("category_id")

    habit_query = db.session.query(Habits).filter(Habits.habit_id==habit_id).first()
    category_query = db.session.query(HabitCategories).filter(HabitCategories.category_id==category_id).first()

    user_id = habit_query.user_id
    if auth_info.user_id == user_id or auth_info.role == 'admin':

        if not habit_query:
            return jsonify({"message": "habit not found"}), 404

        if not category_query:
            return jsonify({"message":"category not found"}),404
    
        if category_query in habit_query.categories:
            return jsonify({"message": "habits already in this category"}), 400
    
        habit_query.categories.append(category_query)

        db.session.commit()
        return jsonify({"message":"habit added to category", "result": habit_schema.dump(habit_query)}),200
    
    return jsonify({"message":"unathorized"}),400



@authenticate_return_auth
def update_habit_by_id(habit_id, auth_info):
    habit_query = db.session.query(Habits).filter(Habits.habit_id == habit_id).first()
    post_data = request.form if request.form else request.json
    user_id = habit_query.user_id

    if not habit_query:
        return jsonify({"message":"habit not found"}), 404

    if auth_info.user_id == user_id:
        populate_obj(habit_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "habit updated", "result": habit_schema.dump(habit_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400



@authenticate_return_auth
def delete_habit_by_id(habit_id, auth_info):
    habit_query = db.session.query(Habits).filter(Habits.habit_id == habit_id).first()
    user_id = habit_query.user_id
    if auth_info.user_id == user_id:
        if not habit_query:
            return jsonify({"message": "no habit with provided id founded."}),404
    
        db.session.delete(habit_query)
        db.session.commit()

        return jsonify({"message":"habit deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
    



