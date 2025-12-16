from flask import Blueprint

import controllers

profile_blueprint = Blueprint('profile_blueprint', __name__)

@profile_blueprint.route('/profile', methods=['POST'])
def add_profile_route():
    return controllers.add_profile()


@profile_blueprint.route('/profiles', methods=['Get'])
def get_all_profiles_route():
    return controllers.get_all_profiles()


@profile_blueprint.route('/profile/<profile_id>', methods=['Get'])
def get_profile_by_id_route(profile_id):
    return controllers.get_profile_by_id(profile_id)


@profile_blueprint.route('/profile/<profile_id>', methods=['PUT'])
def update_profile_by_id_route(profile_id):
    return controllers.update_profile_by_id(profile_id)


@profile_blueprint.route('/profile/delete/<profile_id>', methods=['DELETE'])
def delete_profile_by_id_route(profile_id):
    return controllers.delete_profile_by_id(profile_id)