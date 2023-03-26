# from entities.pets import Pets
from entities.classes import Pets
from models.pets import PetsSchema
from flask import jsonify
from entities.session_database import SessionManager

class PetsCRUD():
    dbSession = SessionManager().session
    pet_schamas = PetsSchema(many=True)
    pet_schama = PetsSchema()

    def getPetList(__self__):
        pet_list = __self__.dbSession.query(Pets).all()
        if len(pet_list) == 0 :
            message = 'There is no lost or found pet yet.'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        else:
            results = __self__.pet_schamas.dump(pet_list)
            return  jsonify(results)
        
    def getPetListWithParams(__self__,params):
        pet_list = __self__.dbSession.query(Pets).all()
        if len(pet_list) == 0 :
            message = 'There is no lost or found pet yet.'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        else:
            try: ## eğer page 1 se offset 0, 2 ise offset perPage(20), 3 ise offset 2*perPage
                    offset = params['PerPage'] * (params['PageSize'] - 1)
                    petListWithPagination =__self__.dbSession.query(Pets).order_by('pet_id').offset(offset).limit(params['PerPage']).all()
                    try:
                        if(params['date_time']):
                            petListWithPagination =__self__.dbSession.query(Pets).order_by('date_time').offset(offset).limit(params['PerPage']).all()
                            results = __self__.pet_schamas.dump(petListWithPagination)
                            return jsonify(results)
                    except:
                        try:
                            if(params['pet_name']): #pagination ile oluyor searchs
                                petListWithPagination =__self__.dbSession.query(Pets).filter_by(pet_name=params['pet_name'])
                                results = __self__.pet_schamas.dump(petListWithPagination)
                                return jsonify(results)
                        except:
                            try:
                                if(params['record_type']):
                                    petListWithPagination =__self__.dbSession.query(Pets).filter_by(record_type=params['record_type'])
                                    results = __self__.pet_schamas.dump(petListWithPagination.offset(offset).limit(params['PerPage']).all())
                                    return jsonify(results)
                            except:
                                try:
                                    if(params['pet_breed']):
                                        petListWithPagination =__self__.dbSession.query(Pets).filter_by(pet_breed=params['pet_breed'])
                                        results = __self__.pet_schamas.dump(petListWithPagination.offset(offset).limit(params['PerPage']).all())
                                        return jsonify(results)
                                except:
                                    results = __self__.pet_schamas.dump(petListWithPagination)
                                    return  jsonify(results)
            except:
                results = __self__.pet_schamas.dump(pet_list)
                return  jsonify(results)
    
    def getPetDetailByPetID(__self__,id):
        pet = __self__.dbSession.query(Pets).get(id)
        if pet :
            return  __self__.pet_schama.jsonify(pet)
        else:
            message = 'Not found pet for this id'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        
    #create_id 'i user sessiondan otamatik al session'u yapınca date'i de oto al
    def createPet(__self__,record_type,date_time,pet_name,pet_breed,pet_color,pet_age,pet_gender,pet_image,pet_details,pet_lost_location,created_id):
        error = __self__.validatePet(record_type,date_time,pet_name,pet_breed,pet_image,pet_lost_location,created_id)
        if error is 'None':
            pet = Pets(record_type,date_time,pet_name,pet_breed,pet_color,pet_age,pet_gender,pet_image,pet_details,pet_lost_location,created_id)
            __self__.dbSession.add(pet)
            __self__.dbSession.commit()
            return __self__.pet_schama.jsonify(pet)
        else:
            return jsonify({'message':error,'status':'500 INTERNAL ERROR'})
    
    def removePet(__self__,id): 
        pet = __self__.dbSession.query(Pets).get(id)
        if pet :
            __self__.dbSession.delete(pet)
            __self__.dbSession.commit()
            return __self__.pet_schama.jsonify(pet)
        else:
            message = 'There is no pet for this id'
            return jsonify({'message':message,'status':'404 NOT FOUND'})

    def editPet(__self__,pet_id,date_time,pet_name,pet_breed,pet_color,pet_age,pet_gender,pet_image,pet_details,pet_lost_location):
        error = __self__.validateEditPet(date_time,pet_name,pet_breed,pet_image,pet_lost_location)
        if error is 'None':
            pet = __self__.dbSession.query(Pets).get(pet_id)
            if pet is None:
                return  jsonify({'message':'There is no pet for this id','status':'404 NOT FOUND'})
            else:
                pet.record_type = pet.record_type
                pet.date_time = date_time
                pet.pet_name = pet_name
                pet.pet_breed = pet_breed
                pet.pet_color = pet_color
                pet.pet_age = pet_age
                pet.pet_gender = pet_gender
                pet.pet_image = pet_image
                pet.pet_gender = pet_gender
                pet.pet_details = pet_details
                pet.pet_lost_location = pet_lost_location
                pet.created_id = pet.created_id
                __self__.dbSession.commit()
                return __self__.pet_schama.jsonify(pet)
        else:
            return jsonify({'message':error,'status':'500 INTERNAL ERROR'})
    
    def changeRecordType(__self__,id,record_type):
        pet = __self__.dbSession.query(Pets).get(id)
        if pet is None:
            return  jsonify({'message':'There is no pet for this id','status':'404 NOT FOUND'})
        else:
            pet.record_type = record_type
            pet.date_time = pet.date_time
            pet.pet_name = pet.pet_name
            pet.pet_breed = pet.pet_breed
            pet.pet_color = pet.pet_color
            pet.pet_age = pet.pet_age
            pet.pet_gender = pet.pet_gender
            pet.pet_image = pet.pet_image
            pet.pet_gender = pet.pet_gender
            pet.pet_details = pet.pet_details
            pet.pet_lost_location = pet.pet_lost_location
            pet.created_id = pet.created_id
            __self__.dbSession.commit()
            return __self__.pet_schama.jsonify(pet)

    def validatePet(__self__,record_type,date_time,pet_name,pet_breed,pet_image,pet_lost_location,created_id):
        error = 'None'
        if not record_type == 0 or record_type == 1 :
            error = 'Record type is required.'
        if not pet_name:
            error = 'Pet name is required.'
        if not pet_breed:
            error = 'Pet breed is required.'
        if not pet_image:
            error = 'Pet image is required.'
        if not pet_lost_location:
            error = 'location is required.'
        if not date_time:
            error = 'Date time is required.'
        if not created_id:
            error = 'Created id is required.'
        return error
    
    def validateEditPet(__self__,date_time,pet_name,pet_breed,pet_image,pet_lost_location):
        error = 'None'
        if not pet_name:
            error = 'Pet name is required.'
        if not pet_breed:
            error = 'Pet breed is required.'
        if not pet_image:
            error = 'Pet image is required.'
        if not pet_lost_location:
            error = 'location is required.'
        if not date_time:
            error = 'Date time is required.'
        return error
    