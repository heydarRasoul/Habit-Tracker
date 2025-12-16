
from flask import request, jsonify

from db import db
from models.habit_reminders import HabitReminders, habitReminder_schema
from util.reflection import populate_obj
from lib.authentication import authenticate_return_auth



@authenticate_return_auth
def add_reminder(auth_info):
    post_data = request.form if request.form else request.json
    user_id = post_data.get('user_id')
    if str(auth_info.user_id) == user_id:

        new_reminder = HabitReminders.new_habitReminder_obj()
        populate_obj(new_reminder, post_data)

        try:
            db.session.add(new_reminder)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message":"unable to add record."}), 400
        
        return jsonify({"message":"reminder added","result": habitReminder_schema.dump(new_reminder)}), 201
    
    return jsonify({"message":"unathorized"}),401



@authenticate_return_auth
def get_reminder_by_id(reminder_id, auth_info):
    reminder_query = db.session.query(HabitReminders).filter(HabitReminders.reminder_id==reminder_id).first()
    user_id = reminder_query.user_id
    if not reminder_query:
        return jsonify({"message":"reminder not found"}), 404
    
    if auth_info.user_id == user_id:
        return jsonify({"message":"reminder found", "result": habitReminder_schema.dump(reminder_query)}), 200

    return  jsonify({"message":"unathorized"}),400



@authenticate_return_auth
def update_reminder_by_id(reminder_id, auth_info):
    reminder_query = db.session.query(HabitReminders).filter(HabitReminders.reminder_id==reminder_id).first()
    post_data = request.form if request.form else request.json
    user_id = reminder_query.user_id
    if not reminder_query:
        return jsonify({"message":"reminder not found"}), 404

    if auth_info.user_id == user_id:
        populate_obj(reminder_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "reminder updated", "result": habitReminder_schema.dump(reminder_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400


@authenticate_return_auth
def delete_reminder_by_id(reminder_id, auth_info):
    reminder_query = db.session.query(HabitReminders).filter(HabitReminders.reminder_id==reminder_id).first()
    user_id = reminder_query.user_id
    if auth_info.user_id == user_id:
        if not reminder_query:
            return jsonify({"message": "no reminder with provided id founded."}),404
    
        db.session.delete(reminder_query)
        db.session.commit()

        return jsonify({"message":"reminder deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
    


