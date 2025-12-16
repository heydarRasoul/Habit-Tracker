from flask import jsonify, request

from db import db
from models.habit_tracking import HabitTracking, habitTracking_schema
from models.habits import Habits
from util.reflection import populate_obj
from lib.authentication import authenticate, authenticate_return_auth



@authenticate_return_auth
def add_track(auth_info):
    post_data = request.form if request.form else request.json
    
    habit_id = post_data.get('habit_id')

    habit_query = db.session.query(Habits).filter(Habits.habit_id == habit_id).first()
    user_id = habit_query.user_id
    if auth_info.user_id == user_id: 

        new_tracker = HabitTracking.new_tracking_obj()
        populate_obj(new_tracker, post_data)

        try:
            db.session.add(new_tracker)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message":"unable to add record."}), 400
            
        return jsonify({"message":"habit tracker added", "result": habitTracking_schema.dump(new_tracker)}), 201
        
    return jsonify({"message":"unathorized"}),401



@authenticate_return_auth
def get_track_by_id(track_id, auth_info):
    track_query = db.session.query(HabitTracking).filter(HabitTracking.track_id==track_id).first()
    if not track_query:
        return jsonify({"message":"habit tracker not found"}), 404

    habit_id = track_query.habit_id

    habit_query = db.session.query(Habits).filter(Habits.habit_id == habit_id).first()
    user_id = habit_query.user_id

    if auth_info.user_id ==user_id: 
        return jsonify({"message":"habit tracker founded", "result": habitTracking_schema.dump(track_query)}), 201
    
    return jsonify({"message":"unathorized"}),401


@authenticate_return_auth
def update_track_by_id(track_id, auth_info):
    post_data = request.form if request.form else request.json
    track_query = db.session.query(HabitTracking).filter(HabitTracking.track_id==track_id).first()
    if not track_query:
        return jsonify({"message":"habit tracker not found"}), 404

    habit_id = track_query.habit_id

    habit_query = db.session.query(Habits).filter(Habits.habit_id == habit_id).first()

    if auth_info.user_id == habit_query.user_id: 
        populate_obj(habit_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "habit tracker updated", "result": habitTracking_schema.dump(track_query )}), 200

    return jsonify({"message":"unathorized"}),401


    

@authenticate_return_auth
def delete_track_by_id(track_id, auth_info):
    track_query = db.session.query(HabitTracking).filter(HabitTracking.track_id==track_id).first()
    if not track_query:
        return jsonify({"message":"habit tracking not found"}), 404

    habit_id = track_query.habit_id

    habit_query = db.session.query(Habits).filter(Habits.habit_id == habit_id).first()

    if auth_info.user.user_id == habit_query.user_id: 
        db.session.delete(track_query)
        db.session.commit()

        return jsonify({"message":"habit tracker deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
