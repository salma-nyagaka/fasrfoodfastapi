'''import modules to create login signup endpoints'''
import datetime
from werkzeug.security import check_password_hash
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from flask_jwt_extended import (jwt_required, get_jwt_identity)



from app.api.v2.model import User
from utils.validators import Validators


class SignUp(Resource):
    '''sigmup a user'''
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="This field cannot be left blank")

    parser.add_argument('email', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True,
                        help="This field cannot be left blank")

    # parser.add_argument('phoneNumber', type=int, required=True,
    #                     help="This field cannot be left blank")
    parser.add_argument('confirm_password', type=str,
                        required=True, help="This field cannot be left blank")
   
   

    def post(self):
        ''' Add a new user '''
        data = SignUp.parser.parse_args()

        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']


        if data['username'].strip() == "":
                return {'message': 'Username cannot be left blank'}, 400                                
        if data['email'].strip() == "":
                return {'message': 'Email cannot be left blank'}, 400                                              
        if data['password'].strip() == "":
                return {'message': 'Password cannot be left blank'}, 400 


        if password != confirm_password:
            return {'message': 'Password do not match'}, 400
        if (len(password) < 6):
            return {'message': 'Password is too short'}, 400
        if (len(username) < 4):
            return {'message': 'Username is too short'}, 400
        if not Validators().valid_account(username):
            return {'message': 'Username can only contain alphanumerics'}, 400
        if not Validators().valid_password(password):
            return {'message': 'Enter valid password'}, 400
        if not Validators().valid_email(email):
            return {'message': 'Enter valid email'}, 400
        # if not Validators().valid_phone(phoneNumber):
        #     return {'message': 'Phone number can only contain + and numbers'}, 400
        if User().get_by_username(username):
            return {'message': 'Username exists'}, 409
        if User().get_by_email(email):
            return {'message': 'Email address exists'}, 409

        user = User(username, email, password)

        user.add()

        return {'message': 'successfully created a new account'}, 201


class Login(Resource):
    '''login a user'''
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="Username field cannot be left blank")
    parser.add_argument('password', type=str, required=True,
                        help="Password field cannot be left blank")

    def post(self):
        ''' login a user '''
        data = Login.parser.parse_args()

        username = data['username']
        username.lower()
        password = data['password']
        if data['username'].strip() == "":
                return {'message': 'Username cannot be left blank'}, 400                                                                            
        if data['password'].strip() == "":
                return {'message': 'Password cannot be left blank'}, 400      

        user = User().get_by_username(username)

        if not user:
            return {'message': 'user does not exist'}, 401

        # if current_user['is_admin']:
        #     admin = True
        # admin = False
            # return {'message': 'Successfully logged in as the admin'}
    
        if not check_password_hash(user.password, password):
            return {'message': 'Wrong password'}, 401
            
        expires = datetime.timedelta(minutes=1200)
        token = create_access_token(identity=user.serialize(),
                                    expires_delta=expires)
        return {
            'token': token,
            'message': 'successfully logged in',
            'admin': user.is_admin
            }, 200


class UpdateProfile(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True,
                        help="This field cannot be left blank")

    parser.add_argument('email', type=str, required=True,
                        help="This field cannot be left blank")
    parser.add_argument('password', type=str, required=True,
                        help="This field cannot be left blank")

    parser.add_argument('phone_number', type=int,
                    required=True, help="This field cannot be left blank")

    @jwt_required
    def put(self, id):
        ''' update user profile'''    
        data = UpdateProfile.parser.parse_args()

        username = data['username']
        email = data['email']
        password = 'password'
        # phone_number = data['phone_number']


        if (len(password) < 6):
            return {'message': 'Password is too short'}, 400
        # if (len(username) < 4):
        #     return {'message': 'Username is too short'}, 400
        if not Validators().valid_account(username):
            return {'message': 'Enter valid username'}, 400
        if not Validators().valid_account(password):
            return {'message': 'Enter valid password'}, 400
        if not Validators().valid_email(email):
            return {'message': 'Enter valid email'}, 400
        return {"message": "profile has been updated"}, 201
