from flask import request, jsonify
from flask_bcrypt import generate_password_hash

from db import db
from models.users import Users, user_schema, users_schema
from util.reflection import populate_obj
from lib.authentication import authenticate_return_auth

def add_user():
    post_data = request.form if request.form else request.json

    new_user = Users.new_user_obj()
    populate_obj(new_user, post_data)

    new_user.password = generate_password_hash(new_user.password).decode('utf-8')

    try:
        db.session.add(new_user)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print("ERROR:", e)
        return jsonify({"message":"unable to add record"}), 400
    
    return jsonify({"message":"user added", "result": user_schema.dump(new_user)}),201



@authenticate_return_auth
def get_all_users(auth_info):
    
    users_query = db.session.query(Users).all()
    if auth_info.user.role =='admin':
        if not users_query:
            return jsonify({"message": "users not founded."}),400

        return jsonify({"message":"users found", "results":users_schema.dump(users_query)}),200

    return jsonify({"message":"unathorized"}),400
  

 
@authenticate_return_auth
def get_user_by_id(user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id == user_id).first()

    if not user_query:
        return jsonify({"message":"user not found"}), 404
    
    if user_id == str(auth_info.user.user_id) or auth_info.user.role == 'admin' :
        return jsonify({"message":"user found", "result": user_schema.dump(user_query)}), 200

    return  jsonify({"message":"unathorized"}),400


@authenticate_return_auth
def get_active_users(auth_info):
    users_query = db.session.query(Users).filter(Users.is_active == True).all()
    if auth_info.user.role =='admin':
        if not users_query:
            return jsonify({"message":"no active user founded"}), 404

        return jsonify({"message":"users founded", "results": users_schema.dump(users_query)}),200 
    
    return jsonify({"message":"unathorized"}),400


@authenticate_return_auth
def update_user_by_id(user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id==user_id).first()
    post_data = request.form if request.form else request.json

    if auth_info.user.role =='admin' or user_id == str(auth_info.user.user_id):
        populate_obj(user_query, post_data)

        db.session.commit()
   
        return jsonify({"message": "user updated", "result": user_schema.dump(user_query)}), 200
    
    return jsonify({"message": "unable to update record"}), 400



@authenticate_return_auth
def delete_user_by_id(user_id, auth_info):
    user_query = db.session.query(Users).filter(Users.user_id==user_id).first()

    if auth_info.user.role == 'admin':
        if not user_query:
            return jsonify({"message": "no user with provided id founded."}),404
    
        db.session.delete(user_query)
        db.session.commit()

        return jsonify({"message":"user deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
    



