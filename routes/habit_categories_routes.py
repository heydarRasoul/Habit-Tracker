from flask import Blueprint
import controllers

category = Blueprint('category', __name__)


@category.route('/category', methods=['POST'])
def add_category_route():
   return controllers.add_category()

@category.route('/categories', methods=['GET'])
def get_all_habitCategories_route():
  return controllers.get_all_habitCategories()


@category.route('/category/<category_id>', methods= ['GET'])
def get_habitCategory_by_id_route(category_id):
    return controllers.get_habitCategory_by_id(category_id)

@category.route('/category/<category_id>', methods=['PUT'])
def update_category_by_id_route(category_id):
   return controllers.update_category_by_id(category_id)

@category.route('/category/delete/<category_id>', methods=['DELETE'])
def delete_category_by_id_route(category_id):
   return controllers.delete_category_by_id(category_id)