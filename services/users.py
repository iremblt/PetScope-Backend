# from entities.users import Users
from models.users import UsersSchema
from models.pets import PetsSchema
from models.userSession import UserSessionSchema
from flask import jsonify
from datetime import datetime, timedelta
import jwt
import bcrypt
import re
from entities.session_database import SessionManager
from entities.classes import Users
from entities.classes import Pets
from entities.userSession import UserSession

class UsersCRUD():
    dbSession = SessionManager().session
    user_schemas = UsersSchema(many=True)
    user_schema = UsersSchema()
    pet_schamas = PetsSchema(many=True)
    user_session_schemas = UserSessionSchema(many=True)
    user_session_schema = UserSessionSchema()

    key = 'lostfoundpets'
    

    def getUserList(__self__):
        user_list = __self__.dbSession.query(Users).all()
        if len(user_list) == 0 :
            message = 'There is no user list.'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        else:
            results = __self__.user_schemas.dump(user_list)
            return jsonify(results)
    
    def getUserByID(__self__,id):
        user = __self__.dbSession.query(Users).get(id)
        if user :
            response = __self__.user_schema.jsonify(user)
            return response
        else:
            message = 'There is no user for this id'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        
    def deleteUser(__self__,id): 
        user = __self__.dbSession.query(Users).get(id)
        if user :
            __self__.dbSession.delete(user)
            __self__.dbSession.commit()
            return __self__.user_schema.jsonify(user)
        else:
            message = 'There is no user for this id'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
    
    def editUser(__self__,id,full_name,telophone_number):
        error = __self__.validateEditUser(full_name)
        if error is 'None':
            user = __self__.dbSession.query(Users).get(id) 
            if user is None:
                return  jsonify({'message':'There is no user this id','success':'404 NOT FOUND'})
            else:
                if full_name:
                    user.full_name = full_name
                else:
                    user.full_name = user.full_name
                user.email = user.email
                user.password = user.password
                if telophone_number:
                    user.telophone_number = telophone_number
                else:
                    user.telophone_number = user.telophone_number
                user.user_type = user.user_type
                user.created_at = user.created_at
                __self__.dbSession.commit()
                response = __self__.user_schema.jsonify(user)
                return response
    
    def changeEmail(__self__,id,email):
        error = __self__.validateEmail(email)
        if error is 'None':
            user = __self__.dbSession.query(Users).get(id) 
            if user is None:
                return  jsonify({'message':'There is no user this id','success':'404 NOT FOUND'})
            else:
                user.full_name = user.full_name
                user.email = email
                user.password = user.password
                user.telophone_number = user.telophone_number
                user.user_type = user.user_type
                user.created_at = user.created_at
                __self__.dbSession.commit()
                response = __self__.user_schema.jsonify(user)
                return response
            
    def changePassword(__self__,id,password):
        error = __self__.validatePassword(password)
        if error is 'None':
            user = __self__.dbSession.query(Users).get(id) 
            if user is None:
                return  jsonify({'message':'There is no user this id','success':'404 NOT FOUND'})
            else:
                user.full_name = user.full_name
                user.email = user.email
                user.password = __self__.encryptPassword(password)
                user.telophone_number = user.telophone_number
                user.user_type = user.user_type
                user.created_at = user.created_at
                __self__.dbSession.commit()
                response = __self__.user_schema.jsonify(user)
                return response
        
    def changeUserType(__self__,id,user_type):
        user = __self__.dbSession.query(Users).get(id) 
        if user is None:
            return  jsonify({'message':'There is no user this id','success':'404 NOT FOUND'})
        else:
            user.full_name = user.full_name
            user.email = user.email
            user.password = user.password
            user.telophone_number = user.telophone_number
            user.user_type = user_type
            user.created_at = user.created_at
            __self__.dbSession.commit()
            response = __self__.user_schema.jsonify(user)
            return response

    def getUserPetFlyers(__self__,id):
        user = __self__.dbSession.query(Users).get(id) 
        if user is None :
            return jsonify({'message':'There is no user this id','success':'404 NOT FOUND'})
        else:
            if user.pets is None:
                return jsonify({'message':'This user has not pet flyer','success':'404 NOT FOUND'})
            else:
                user_flayers = __self__.dbSession.query(Pets).filter_by(created_id=id)
                response = __self__.pet_schamas.jsonify(user_flayers)
                return response
            
                    
    def login(__self__,email,password): 
        error = __self__.validateLoginUser(email,password)
        if error is 'None':
            user = __self__.dbSession.query(Users).filter_by(email=email).first()
            if user is None:
                jsonify({'message':'There is no user','success':'404 NOT FOUND'})
            else:
                password = __self__.decryptPassword(password,user.password)
                if password is False:
                    jsonify({'message':'Password is wrong','success':'404 NOT FOUND'})
                else:
                    payload = {
                        'userId': user.user_id,
                        'user_name': user.full_name,
                        'email': user.email,
                        'exp': datetime.utcnow() + timedelta(seconds=20)
                        }
                    jwt_token = jwt.encode(payload, __self__.key,algorithm='HS256')
                    jwtDecoded = jwt.decode(jwt_token,__self__.key,algorithms='HS256')
                    response = {
                        'token' : jwt_token,
                        'userId': user.user_id,
                        'user_name': user.full_name,
                        'email': user.email,
                        'exp': datetime.utcnow() + timedelta(seconds=20)
                    }
                    __self__.createUserSessionOnDatabase(user.user_id, jwt_token)
                    return response
        else:
            return jsonify({'message':error,'success':'500 INTERNAL ERROR'})
        
    def createUserSessionOnDatabase(__self__, userId, jwToken):
        userSession = UserSession(userId,datetime.now(), datetime.now() + timedelta(hours=24), False, jwToken)
        __self__.dbSession.add(userSession)
        __self__.dbSession.commit()
    
    def getActiveSession(__self__, jwt):
        now = datetime.now()
        #expire_date > now,
        filtered = __self__.dbSession.query(UserSession).filter_by(jw_token=jwt, logged_out = False)
        active = filtered.first()

        if active is not None:
            user = __self__.dbSession.query(Users).get(active.user_id)
            response = __self__.user_schema.jsonify(user)
            return response
        else:
            return None

    def logout(self, jwt):
        if jwt is not None:
            current_session = self.dbSession.query(UserSession).filter_by(jw_token=jwt).first()
            if current_session is not None:
                if current_session.logged_out == False:
                    current_session.logged_out = True
                    self.dbSession.commit()
                return jsonify({'message':'Log out successfully','success':'200 OK'})
        
        return jsonify({'message':'Something went wrong!','success':'500 INTERNAL ERROR'})

    def register(__self__,full_name,email,password,telophone_number,user_type,created_at):
        error = __self__.validateRegisterUser(email,password,full_name,user_type,created_at)
        if error is 'None':
            password = __self__.encryptPassword(password)
            user = Users(full_name, email, password, telophone_number,user_type,created_at)
            __self__.dbSession.add(user)
            __self__.dbSession.commit()
            return __self__.user_schema.jsonify(user)
        else:
            return jsonify({'message':error,'success':'500 INTERNAL ERROR'})
    
    def encryptPassword(__self__,password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def decryptPassword(__self__,password,realpassword):
        return bcrypt.checkpw(password.encode('utf-8'), realpassword.encode('utf-8'))
    
    def validateLoginUser(__self__,email,password):
        error = 'None'
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])"
        if not email:
            error = 'Email is required.'
        elif not re.fullmatch(regex, email):
            error = 'Email is not valid.'
        elif not password:
            error = 'Password is required.'
        elif len(password) < 8:
            error = 'Password length must be 8.'
        elif not re.match(password_pattern, password):
            error = 'Password must be one uppercase and lowercase and one digit character and one special character'
        result = __self__.dbSession.query(Users).filter_by(email=email).first()
        if result is None:
            error = 'User is not exist. Your email or password wrong.'
        return error
    
    def validateRegisterUser(__self__,email,password,full_name,user_type,created_at):
        error = 'None'
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])"
        if not full_name:
            error = 'Full name is required.'
        elif not user_type:
            error = 'User type is required.'
        elif not created_at:
            error = 'Created date sis required.'
        elif not email:
            error = 'Email is required.'
        elif not re.fullmatch(regex, email):
            error = 'Email is not valid.'
        elif not password:
            error = 'Password is required.'
        elif len(password) < 8:
            error = 'Password length must be 8.'
        elif not re.match(password_pattern, password):
            error = 'Password must be one uppercase and lowercase and one digit character and one special character'
        result = __self__.dbSession.query(Users).filter_by(email=email).first()
        if result is not None:
            error = 'User is already exist. Your email is already using.'
        return error

    def validateEditUser(__self__,full_name):
        error = 'None'
        if not full_name:
            error = 'Full name is required.'
        return error
    
    def validateEmail(__self__,email):
        error = 'None'
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not email:
            error = 'Email is required.'
        elif not re.fullmatch(regex, email):
            error = 'Email is not valid.'
        result = __self__.dbSession.query(Users).filter_by(email=email).first()
        if result is not None:
            error = 'This email is already using'
        return error
    
    def validatePassword(__self__,password):
        error = 'None'
        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])"
        if not password:
            error = 'Password is required.'
        elif len(password) < 8:
            error = 'Password length must be 8.'
        elif not re.match(password_pattern, password):
            error = 'Password must be one uppercase and lowercase and one digit character and one special character'
        return error