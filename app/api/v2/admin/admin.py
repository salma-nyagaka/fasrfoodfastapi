''' module imports'''
from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, get_jwt_identity)


from utils.validators import Validators
from app.api.v2.model import FoodOrder, FoodMenu


class PlaceNewMenu(Resource):
    '''place a new food menu item'''
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True,
                        help="This field cannot be left blank")

    parser.add_argument('description', type=str, required=True,
                        help="This field cannot be left blank")

    parser.add_argument('price', type=str, required=True,
                        help="Enter valid price")

    parser.add_argument('image', type=str, required=True,
                        help="image cannot be left blank")



    @jwt_required
    def post(self):
        ''' place new menu'''
        current_user = get_jwt_identity()

        if current_user['is_admin']:
            data = PlaceNewMenu.parser.parse_args()
            name = data['name']
            description = data['description']
            price = data['price']
            image = data['image']


            if data['name'].strip() == "":
                return {'message': 'Name cannot be left blank'}, 400
            if data['description'].strip() == "":
                return {'message': 'Description cannot be left blank'}, 400                                

            if not Validators().valid_food(name):
                return {'message': 'Enter valid food name'}, 400
            if not Validators().valid_food(description):
                return {'message': 'Enter valid food description'}, 400
            if FoodMenu().get_by_name(name):
                return {'message': 'This food already exists'}, 409
            menu = FoodMenu(name=name, description=description, price=price, image=image)
            menu.add()
            meal = FoodMenu().get_by_name(name)
            return {"message": "Food menu created", "meal":meal.serialize()}, 201
        return {"message": "Insufficient permissions to add a new meal item"}, 403


class AllMenu(Resource):
    '''get all menu'''
    @jwt_required
    def get(self):
        """ Get all food items """
        current_user = get_jwt_identity()

        if current_user['is_admin']:
            data = FoodMenu().get_all()

            food_menus = []

            if data:
                for food_menu in data:
                    food_menus.append(food_menu.serialize())

                return {"Food menu": food_menus,
                        "message": "These are meals"}, 200

            return {"message": "No food items available for now"}, 404
        return {"message": "Insufficient permissions to view this section"}, 403



class DeleteMenu(Resource):
    '''get specific menu'''
    @jwt_required
    def delete(self, id):
        ''' Delete a specific menu '''
        current_user = get_jwt_identity()

        if current_user['is_admin']:
            menu = FoodMenu().get_by_id(id)
            if menu:
                menu.delete(id)
                return {'message': "Successfully Deleted"}, 200
            return {'message': "Menu item not found"}, 404
        return {"message": "Insufficient permissions to perform this actions"}, 403




class SpecificMenu(Resource):
    '''get specific menu'''
    @jwt_required
    def get(self, id):
        ''' gets a specific menu'''
        menu = FoodMenu().get_by_id(id)

        if menu:
            return {"Menu": menu.serialize(),
                    "message": "These are the available food menu"}, 200
        return {'message': "Not found"}, 404


class AllUserOrders(Resource):
    '''get all the orders made by users'''
    @jwt_required
    def get(self):
        ''' get all food orders '''
        current_user = get_jwt_identity()

        if current_user['is_admin']:

            foodorder = FoodOrder()
            if foodorder.get_all():
                return {'Food Orders': [foodorder.serialize() for foodorder
                                        in foodorder.get_all()]}, 200
            return {'message': "No orders have been made"}, 404
        return {"message": "Insufficient permissions to view this page"}, 403


class FilterOrdersByStatus(Resource):
    '''get all the orders made by users'''
    @jwt_required
    def get(self, status):
        ''' get all food orders '''
        current_user = get_jwt_identity()
        
        if current_user['is_admin']:

            foodorders = FoodOrder().get_all()
            
            if foodorders:
                orders = [order.serialize() for order in foodorders if order.status == status]

                if orders:
                    return {'Updated orders': orders}, 200
                return {'message': "No orders found"}, 404
            return {'message': "No orders found"}, 404
        return {"message": "Insufficient permissions to perform this actions"}, 403





class GetSpecificOrder(Resource):
    '''get a specific user order'''
    @jwt_required
    def get(self, id):
        ''' get a specific order '''

        order = FoodOrder().get_by_id(id)
        if order:
            return {"message": "Specific order", "order":order.serialize()}, 200
        return {'message': "Not found"}, 404


class UpdateStatus(Resource):
    '''upodate order status'''
    parser = reqparse.RequestParser()
    parser.add_argument('status', type=str, required=True,
                        help="Enter valid status")
    @jwt_required
    def put(self, id):
        '''update status to accept, decline, complete'''
        current_user = get_jwt_identity()

        if current_user['is_admin']:

            data = UpdateStatus.parser.parse_args()
            order = FoodOrder().get_by_id(id)

            if order:
                status = data['status']
                order.update_order(status, id)
                new_order = FoodOrder().get_by_id(id)
                return{"order":  new_order.serialize()}, 200
            
            return{'message': "No orders yet"}, 404
        return {"message": "Insufficient permissions to perform this actions"}, 403

class UpdateMeal(Resource):

    @jwt_required
    def put(self, id):
        ''' update a meal'''
        current_user = get_jwt_identity()

        if current_user['is_admin']:
            data = PlaceNewMenu.parser.parse_args()
            name = (data['name']).lower()
            description = data['description']
            image = data['image']
            price = data['price']

            if not Validators().valid_food(name):
                return {'message': 'Enter valid food name'}, 400
            if not Validators().valid_food(description):
                return {'message': 'Enter valid food description'}, 400

            if FoodMenu().get_by_id(id):
                menu = FoodMenu(name=name, description=description, price=price, image=image)
                # menu.add()
                menu.update(id)
            return {"message": "Food menu updated"}, 201
        return {"message": "Insufficient permissions to perform this actions"}, 403


class GetMeal(Resource):
    '''get a specific meal'''
    @jwt_required
    def get(self, name):
        ''' get a specific order '''

        meal = FoodMenu().get_by_name(name)
        if meal:
            return {"message": "Specific meal", "meal":meal.serialize()}, 200
        return {'message': "Not found"}, 404
