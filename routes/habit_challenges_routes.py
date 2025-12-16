from flask import Blueprint

import controllers

challenges_blueprint = Blueprint('challenges_blueprint', __name__)

@challenges_blueprint.route('/challenge', methods=['POST'])
def add_challenge_route():
    return controllers.add_challenge()


@challenges_blueprint.route('/challenges', methods=['GET'])
def get_all_challenges_route():
    return controllers.get_all_challenges()

@challenges_blueprint.route('/challenge/user', methods=['POST'])
def add_user_to_challenge_route():
    return controllers.add_user_to_challenge()


@challenges_blueprint.route('/challenge/<challenge_id>', methods=['GET'])
def get_challenge_by_id_route(challenge_id):
    return controllers.get_challenge_by_id(challenge_id)


@challenges_blueprint.route('/challenge/<challenge_id>', methods=['PUT'])
def update_challenge_by_id_route(challenge_id):
    return controllers.update_challenge_by_id(challenge_id)


@challenges_blueprint.route('/challenge/delete/<challenge_id>', methods=['DELETE'])
def delete_challenge_by_id_route(challenge_id):
    return controllers.delete_challenge_by_id(challenge_id)