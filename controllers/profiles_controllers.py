from flask import request, jsonify

from db import db
from models.profiles import Profiles, profile_schema, profiles_schema
from util.reflection import populate_obj
from lib.authentication import authenticate_return_auth, authenticate


@authenticate_return_auth
def add_profile(auth_info):
    post_data = request.form if request.form else request.json
    user_id = post_data.get('user_id')
    if str(auth_info.user.user_id) == user_id:

        new_profile = Profiles.new_profile_obj()
        populate_obj(new_profile, post_data)

        try:
            db.session.add(new_profile)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message":"unable to add record."}), 400
        
        return jsonify({"message":"profile added","result": profile_schema.dump(new_profile)}), 201
    
    return jsonify({"message":"unathorized"}),401


@authenticate_return_auth
def get_all_profiles(auth_info):
    profile_query = db.session.query(Profiles).all()

    if not profile_query:
        return jsonify({"message":"profiles not found"}), 404
    
    if auth_info.user.role == 'admin':
        return jsonify({"message":"profiles found", "result": profiles_schema.dump(profile_query)}), 200



@authenticate
def get_profile_by_id(profile_id):
    profile_query = db.session.query(Profiles).filter(Profiles.profile_id == profile_id).first()

    if not profile_query:
        return jsonify({"message":"profile not found"}), 404
   
    return jsonify({"message":"profile found", "result": profile_schema.dump(profile_query)}), 200



@authenticate_return_auth
def update_profile_by_id(profile_id, auth_info):
    profile_query = db.session.query(Profiles).filter(Profiles.profile_id == profile_id).first()
    post_data = request.form if request.form else request.json

    if auth_info.user_id == profile_query.user_id:
        populate_obj(profile_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "profile updated", "result": profile_schema.dump(profile_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400




@authenticate_return_auth
def delete_profile_by_id(profile_id, auth_info):
    profile_query = db.session.query(Profiles).filter(Profiles.profile_id == profile_id).first()

    if not profile_query:
        return jsonify({"message": "no profile with provided id founded."}),404
    
    if auth_info.user_id == profile_query.user_id or auth_info.user.role == 'admin':
        db.session.delete(profile_query)
        db.session.commit()

        return jsonify({"message":"profile deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
    





