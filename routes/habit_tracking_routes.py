from flask import Blueprint

import controllers

tracking_blueprint = Blueprint('tracking_blueprint', __name__)


@tracking_blueprint.route('/tracking', methods=['POST'])
def add_track_route():
    return controllers.add_track()


@tracking_blueprint.route('/tracking/<track_id>', methods=['GET'])
def get_track_by_id_route(track_id):
    return controllers.get_track_by_id(track_id)


@tracking_blueprint.route('/tracking/<track_id>', methods=['PUT'])
def update_track_by_id_route(track_id):
    return controllers.update_track_by_id(track_id)


@tracking_blueprint.route('/tracking/delete/<track_id>', methods=['DELETE'])
def delete_track_by_id_route(track_id):
    return controllers.delete_track_by_id(track_id)