from flask import Blueprint

import controllers

auth_token_blueprint = Blueprint('auth_token', __name__)

@auth_token_blueprint.routes('/user/auth', methods=['POST'])
def auth_token_add_route():
    return controllers.auth_token_add()

@auth_token_blueprint.routes('/logout', methods=['DELETE'])
def auth_token_delete():
    return controllers.auth_token_delete()