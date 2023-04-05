from flask import Flask
import flask_login
from flask import Flask, session,request
from datetime import datetime
from services.pets import PetsCRUD
from services.users import UsersCRUD


app = Flask(__name__)
app.secret_key = 'lostfoundpets'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

petServices = PetsCRUD()
userServices= UsersCRUD()

@app.route('/', methods=(['GET']))
def home():
    return 'Hello'

@app.route('/Pet/List', methods=(['GET']))
def petList():
    try:
        if(getattr(request, 'json', None)):
                try:
                    if(request.json['pet_name']):  
                        petList = petServices.searchPetListByName(params={
                            'PageSize': request.json['PageSize'],'PerPage':request.json['PerPage'],
                            'pet_name': request.json['pet_name']
                            })
                        return petList
                except:
                    try:
                        if(request.json['record_type']):
                            petList = petServices.filterByRecordType(params={
                                'PageSize': request.json['PageSize'],'PerPage':request.json['PerPage'],
                                'record_type': request.json['record_type']
                                })
                            return petList
                    except:
                        try:
                            if(request.json['pet_breed']):  
                                petList = petServices.filterByPetBreed(params={
                                    'PageSize': request.json['PageSize'],'PerPage':request.json['PerPage'],
                                    'pet_breed': request.json['pet_breed']
                                    })
                                return petList
                        except:
                            try:
                                if(request.json['pet_lost_location']):
                                    petList = petServices.filterByPetLocation(params={
                                        'PageSize': request.json['PageSize'],'PerPage':request.json['PerPage'],
                                        'pet_lost_location': request.json['pet_lost_location']
                                        })
                                    return petList
                            except:
                                try:
                                    if(request.json['pet_age']):
                                        petList = petServices.filterByPetAge(params={
                                            'PageSize': request.json['PageSize'],'PerPage':request.json['PerPage'],
                                            'pet_age': request.json['pet_age']
                                            })
                                        return petList
                                except:
                                    try:
                                        if(request.json['pet_color']):
                                            petList = petServices.filterByPetColor(params={
                                            'PageSize': request.json['PageSize'],'PerPage':request.json['PerPage'],
                                            'pet_color': request.json['pet_color']
                                            })
                                            return petList
                                    except:
                                        try:
                                            if(request.json['pet_gender']):
                                                petList = petServices.filterByPetGender(params={
                                                'PageSize': request.json['PageSize'],'PerPage':request.json['PerPage'],
                                                'pet_gender': request.json['pet_gender']
                                                })
                                                return petList
                                        except:
                                            petList = petServices.getPetListWithPagination(params={
                                            'PageSize': request.json['PageSize'],'PerPage':request.json['PerPage']
                                            })
                                            return petList
    except:
        petList = petServices.getPetList()
        return petList

@app.route('/Pet/List', methods=(['GET']))
def petListWithSearchByName():
    petList = petServices.getPetList()
    return petList

@app.route('/Pet/Detail/<id>', methods=(['GET']))
def getDetailPet(id):
    pet = petServices.getPetDetailByPetID(id)
    return pet

@app.route('/Pet/Remove/<id>', methods=(['DELETE']))
def deletePet(id):
    pet = petServices.removePet(id)
    return pet

@app.route('/Pet/Update/<id>', methods=(['PUT']))
def updatePet(id):
    date_time = request.json['date_time']
    pet_name = request.json['pet_name']
    pet_breed = request.json['pet_breed']
    pet_color = request.json['pet_color']
    pet_age = request.json['pet_age']
    pet_gender = request.json['pet_gender']
    pet_image = request.json['pet_image']
    pet_details = request.json['pet_details']
    pet_lost_location = request.json['pet_lost_location']
    pet = petServices.editPet(id,date_time,pet_name,pet_breed,pet_color,pet_age,pet_gender,pet_image,pet_details,pet_lost_location)
    return pet

@app.route('/Pet/Change/Status/<id>', methods=(['PUT']))
def cahngeStatus(id):
    record_type = request.json['record_type']
    pet = petServices.changeRecordType(id,record_type)
    return pet

@app.route('/Pet/Add', methods=(['POST']))
def addNewPet():
    record_type = request.json['record_type']
    date_time = request.json['date_time']
    pet_name= request.json['pet_name']
    pet_breed= request.json['pet_breed']
    pet_color= request.json['pet_color']
    pet_age= request.json['pet_age']
    pet_gender= request.json['pet_gender']
    pet_image= request.json['pet_image']
    pet_details= request.json['pet_details']
    pet_lost_location= request.json['pet_lost_location']
    created_id= request.json['created_id']
    pet = petServices.createPet(record_type,date_time,pet_name,pet_breed,pet_color,pet_age,pet_gender,pet_image,pet_details,pet_lost_location,created_id)
    return pet

@app.route('/Pet/Recommendation', methods=(['POST']))
def recommendPet():
    record_type = request.json['record_type']
    date_time = request.json['date_time']
    pet_name= request.json['pet_name'] or None
    pet_breed= request.json['pet_breed']
    pet_color= request.json['pet_color'] or None
    pet_age= request.json['pet_age'] or None
    pet_gender= request.json['pet_gender'] or None
    pet_image= request.json['pet_image']
    pet_details= request.json['pet_details'] or None
    pet_lost_location= request.json['pet_lost_location']
    created_id= request.json['created_id']
    pet = petServices.recommendPet(record_type,date_time,pet_name,pet_breed,pet_color,pet_age,pet_gender,pet_image,pet_details,pet_lost_location,created_id)
    return pet

@app.route('/User/List', methods=(['GET']))
def userList():
    userList = userServices.getUserList()
    return userList

@app.route('/User/Detail/<id>', methods=(['GET']))
def getDetailUser(id):
    user = userServices.getUserByID(id)
    return user

@app.route('/User/Remove/<id>', methods=(['DELETE']))
def deleteUser(id):
    user = userServices.deleteUser(id)
    return user

@app.route('/User/Update/<id>', methods=(['PUT']))
def updateUser(id):
    full_name = request.json['full_name']
    telophone_number = request.json['telophone_number']
    user = userServices.editUser(id,full_name,telophone_number)
    return user

@app.route('/User/<id>/Change/Email', methods=(['PUT']))
def changeEmail(id):
    email = request.json['email']
    user = userServices.changeEmail(id,email)
    return user

@app.route('/User/Add', methods=(['POST']))
def register():
    full_name = request.json['full_name']
    email = request.json['email']
    password = request.json['password']
    telophone_number = request.json['telophone_number']
    user_type = request.json['user_type']
    created_at = datetime.utcnow()
    user = userServices.register(full_name,email,password,telophone_number,user_type,created_at)
    return user

@app.route('/User/Login', methods=(['POST']))
def login():
    email = request.json['email']
    password = request.json['password']
    user = userServices.login(email,password)
    session['userSession'] = user['token']
    print(session['userSession'])
    return user

@app.route('/User/Logout', methods=(['POST']))
def logout():
    user = userServices.logout(session['userSession'])
    session.pop('userSession', None)
    return user

@app.route('/User/Active/User', methods=(['GET']))
def getActiveUser():
    user = userServices.getActiveSession(session['userSession'])
    return user


@app.route('/User/<id>/Change/Password', methods=(['PUT']))
def changePassword(id):
    password = request.json['password']
    user = userServices.changePassword(id,password)
    return user

@app.route('/User/<id>/Change/Status', methods=(['PUT']))
def changeStatus(id):
    password = request.json['user_type']
    user = userServices.changeUserType(id,password)
    return user

@app.route('/User/<id>/Get/Flyers', methods=(['GET']))
def getUserFlyers(id):
    user = userServices.getUserPetFlyers(id)
    return user


app.run()