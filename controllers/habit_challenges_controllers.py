from flask import request, jsonify

from db import db
from models.habit_challenges import HabitChallenges, habitChallenge_schema, habitChallenges_schema
from models.users import Users
from util.reflection import populate_obj
from lib.authentication import authenticate_return_auth, authenticate



@authenticate_return_auth
def add_challenge(auth_info):
    post_data = request.form if request.form else request.json
    if auth_info.user.role == 'admin':
        new_challenge = HabitChallenges.new_habitChallenge_obj()
        populate_obj(new_challenge, post_data)

        try:
            db.session.add(new_challenge)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message":"unable to add record."}), 400
        
    return jsonify({"message":"challenge added","result": habitChallenge_schema.dump(new_challenge)}), 201


@authenticate_return_auth
def add_user_to_challenge(auth_info):
    post_data = request.form if request.form else request.json
    
    challenge_id= post_data.get('challenge_id')
    user_id = post_data.get('user_id')

    user_query = db.session.query(Users).filter(Users.user_id==user_id).first()
    challenge_query = db.session.query(HabitChallenges).filter(HabitChallenges.challenge_id==challenge_id).first()
    if str(auth_info.user_id) == user_id or auth_info.role=='admin':

        if not user_query:
            return jsonify({"message": "user not found"}), 404

        if not challenge_query:
            return jsonify({"message":"challenge not found"}),404
    
        if user_query in challenge_query.users:
            return jsonify({"message": "user already in this challenge"}), 400
    
        challenge_query.users.append(user_query)


        db.session.commit()
        return jsonify({"message":"user added to challenge", "result": habitChallenge_schema.dump(challenge_query)}),200
    
    return jsonify({"message":"unathorized"}),400


@authenticate
def get_all_challenges():
    
    challenge_query = db.session.query(HabitChallenges).all()
    if not challenge_query:
        return jsonify({"message": "no challenge founded."}),400

    return jsonify({"message":"challenges found", "results":habitChallenges_schema.dump(challenge_query)}),200



@authenticate
def get_challenge_by_id(challenge_id):
    
    challenge_query = db.session.query(HabitChallenges).filter(HabitChallenges.challenge_id==challenge_id).first()
    if not challenge_query:
        return jsonify({"message": "no challenge founded."}),400

    return jsonify({"message":"challenges found", "results":habitChallenge_schema.dump(challenge_query)}),200


@authenticate_return_auth
def update_challenge_by_id(challenge_id, auth_info):
    post_data = request.form if request.form else request.json
    challenge_query = db.session.query(HabitChallenges).filter(HabitChallenges.challenge_id==challenge_id).first()
    if auth_info.user.role == 'admin':
        if not challenge_query:
            return jsonify({"message":"challenge not found"}), 404
        
        populate_obj(challenge_query, post_data)
        db.session.commit()

        return jsonify({"message":"challenge updated","result": habitChallenge_schema.dump(challenge_query)}), 201

    return jsonify({"message":"unathorized"}),400
    

@authenticate_return_auth
def delete_challenge_by_id(challenge_id, auth_info):
    challenge_query = db.session.query(HabitChallenges).filter(HabitChallenges.challenge_id==challenge_id).first()

    if auth_info.user.role == 'admin':
        if not challenge_query:
            return jsonify({"message": "no habit with provided id founded."}),404
    
        db.session.delete(challenge_query)
        db.session.commit()

        return jsonify({"message":"challenge deleted"}),200
    
    return jsonify({"message":"unathorized"}),400
    




    
    