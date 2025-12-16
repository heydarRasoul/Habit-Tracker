from flask import Blueprint

import controllers

reminders_blueprint = Blueprint('reminders_blueprint', __name__)

@reminders_blueprint.route('/reminder', methods=['POST'])
def add_reminder_route():
    return controllers.add_reminder()


@reminders_blueprint.route('/reminder/<reminder_id>', methods=['GET'])
def get_reminder_by_id_route(reminder_id):
    return controllers.get_reminder_by_id(reminder_id)


@reminders_blueprint.route('/reminder/<reminder_id>', methods=['PUT'])
def update_reminder_by_id_route(reminder_id):
    return controllers.update_reminder_by_id(reminder_id)



@reminders_blueprint.route('/reminder/<reminder_id>', methods=['DELETE'])
def delete_reminder_by_id_route(reminder_id):
    return controllers.delete_reminder_by_id(reminder_id)
