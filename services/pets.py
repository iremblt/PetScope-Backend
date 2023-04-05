# from entities.pets import Pets
from entities.classes import Pets
from models.pets import PetsSchema
from flask import jsonify
from entities.session_database import SessionManager
import pandas as pd
import nltk
import re
import string
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.metrics.pairwise import cosine_similarity
import json

nltk.download('stopwords')
nltk.download('wordnet')

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
        
    def getPetListWithPagination(__self__,params):
        pet_list = __self__.dbSession.query(Pets).all()
        if len(pet_list) == 0 :
            message = 'There is no lost or found pet yet.'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        else:
            try: ## eğer page 1 se offset 0, 2 ise offset perPage(20), 3 ise offset 2*perPage
                    offset = params['PerPage'] * (params['PageSize'] - 1)
                    petListWithPagination =__self__.dbSession.query(Pets).order_by('date_time').offset(offset).limit(params['PerPage']).all()
                    results = __self__.pet_schamas.dump(petListWithPagination)
                    return  jsonify(results)
            except:
                results = __self__.pet_schamas.dump(pet_list)
                return  jsonify(results)
            
    def searchPetListByName(__self__,params):
        pet_list = __self__.dbSession.query(Pets).all()
        if len(pet_list) == 0 :
            message = 'There is no lost or found pet yet.'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        else:
            pet_list_search =__self__.dbSession.query(Pets).filter(Pets.pet_name.contains(params['pet_name'])).all()
            if len(pet_list_search) == 0 :
                message = 'There is no pets name in your search query.'
                return jsonify({'message':message,'success':'404 NOT FOUND'})
            else:
                offset = params['PerPage'] * (params['PageSize'] - 1)
                pet_list_pagination = __self__.dbSession.query(Pets).filter(Pets.pet_name.contains(params['pet_name'])).order_by('date_time').offset(offset).limit(params['PerPage']).all()
                results = __self__.pet_schamas.dump(pet_list_pagination)
                response = jsonify(results)
                return response
    
    def filterByRecordType(__self__,params):
        pet_list = __self__.dbSession.query(Pets).all()
        if len(pet_list) == 0 :
            message = 'There is no lost or found pet yet.'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        else:
            pet_list_filter =__self__.dbSession.query(Pets).filter_by(record_type=params['record_type'])
            if len(pet_list_filter) == 0 :
                message = 'There is no pets name in your record type.'
                return jsonify({'message':message,'success':'404 NOT FOUND'})
            else:
                offset = params['PerPage'] * (params['PageSize'] - 1)
                pet_list_pagination = __self__.dbSession.query(Pets).filter_by(record_type=params['record_type']).order_by('date_time').offset(offset).limit(params['PerPage']).all()
                results = __self__.pet_schamas.dump(pet_list_pagination)
                response = jsonify(results)
                return response
    
    def filterByPetBreed(__self__,params):
        pet_list = __self__.dbSession.query(Pets).all()
        if len(pet_list) == 0 :
            message = 'There is no lost or found pet yet.'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        else:
            pet_list_filter =__self__.dbSession.query(Pets).filter_by(pet_breed=params['pet_breed'])
            if len(pet_list_filter) == 0 :
                message = 'There is no pets in this breed.'
                return jsonify({'message':message,'success':'404 NOT FOUND'})
            else:
                offset = params['PerPage'] * (params['PageSize'] - 1)
                pet_list_pagination = __self__.dbSession.query(Pets).filter_by(pet_breed=params['pet_breed']).order_by('date_time').offset(offset).limit(params['PerPage']).all()
                results = __self__.pet_schamas.dump(pet_list_pagination)
                response = jsonify(results)
                return response
    
    def filterByPetLocation(__self__,params):
        pet_list = __self__.dbSession.query(Pets).all()
        if len(pet_list) == 0 :
            message = 'There is no lost or found pet yet.'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        else:
            pet_list_filter =__self__.dbSession.query(Pets).filter(Pets.pet_lost_location.contains(params['pet_lost_location'])).all()
            if len(pet_list_filter) == 0 :
                message = 'There is no pets in this this location.'
                return jsonify({'message':message,'success':'404 NOT FOUND'})
            else:
                offset = params['PerPage'] * (params['PageSize'] - 1)
                pet_list_pagination = __self__.dbSession.query(Pets).filter(Pets.pet_lost_location.contains(params['pet_lost_location'])).order_by('date_time').offset(offset).limit(params['PerPage']).all()
                results = __self__.pet_schamas.dump(pet_list_pagination)
                response = jsonify(results)
                return response
            
    def filterByPetAge(__self__,params):
        pet_list = __self__.dbSession.query(Pets).all()
        if len(pet_list) == 0 :
            message = 'There is no lost or found pet yet.'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        else:
            pet_list_filter =__self__.dbSession.query(Pets).filter_by(pet_age=params['pet_age'])
            if len(pet_list_filter) == 0 :
                message = 'There is no pets in this age.'
                return jsonify({'message':message,'success':'404 NOT FOUND'})
            else:
                offset = params['PerPage'] * (params['PageSize'] - 1)
                pet_list_pagination = __self__.dbSession.query(Pets).filter_by(pet_age=params['pet_age']).order_by('date_time').offset(offset).limit(params['PerPage']).all()
                results = __self__.pet_schamas.dump(pet_list_pagination)
                response = jsonify(results)
                return response
            
    def filterByPetColor(__self__,params):
        pet_list = __self__.dbSession.query(Pets).all()
        if len(pet_list) == 0 :
            message = 'There is no lost or found pet yet.'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        else:
            pet_list_filter =__self__.dbSession.query(Pets).filter_by(pet_color=params['pet_color'])
            if len(pet_list_filter) == 0 :
                message = 'There is no pets in this color.'
                return jsonify({'message':message,'success':'404 NOT FOUND'})
            else:
                offset = params['PerPage'] * (params['PageSize'] - 1)
                pet_list_pagination = __self__.dbSession.query(Pets).filter_by(pet_color=params['pet_color']).order_by('date_time').offset(offset).limit(params['PerPage']).all()
                results = __self__.pet_schamas.dump(pet_list_pagination)
                response = jsonify(results)
                return response
            
    def filterByPetGender(__self__,params):
        pet_list = __self__.dbSession.query(Pets).all()
        if len(pet_list) == 0 :
            message = 'There is no lost or found pet yet.'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        else:
            pet_list_filter =__self__.dbSession.query(Pets).filter_by(pet_gender=params['pet_gender'])
            if len(pet_list_filter) == 0 :
                message = 'There is no pets in this gender.'
                return jsonify({'message':message,'success':'404 NOT FOUND'})
            else:
                offset = params['PerPage'] * (params['PageSize'] - 1)
                pet_list_pagination = __self__.dbSession.query(Pets).filter_by(pet_gender=params['pet_gender']).order_by('date_time').offset(offset).limit(params['PerPage']).all()
                results = __self__.pet_schamas.dump(pet_list_pagination)
                response = jsonify(results)
                return response

    def dataCleaning(__self__,data):
        lemmatizer = WordNetLemmatizer()
        stopWords = set(stopwords.words('english'))
        for punctuation in string.punctuation:
            item = data[0].replace(punctuation, ' ')
        item = re.split(' ', item)
        item = [word for word in item if word.isalpha()]
        item = [word.lower() for word in item]
        item = [lemmatizer.lemmatize(word) for word in item]
        item = [word for word in item if word not in stopWords]
        return ' '.join(item)
    
    def locationCleaning(__self__,data):
        lemmatizer = WordNetLemmatizer()
        stopWords = set(stopwords.words('english'))
        for punctuation in string.punctuation:
            item = data[0].replace(punctuation, ' ')
        item = re.split('/', item)
        item = [word for word in item if word.isalpha()]
        item = [word.lower() for word in item]
        item = [lemmatizer.lemmatize(word) for word in item]
        item = [word for word in item if word not in stopWords]
        return ' '.join(item)
    
    def dateTimeCleaning(__self__,data):
        item = data[0]
        item = re.split(' ', item)
        return ' '.join(item)

    def inputCleaning(__self__,data):
        lemmatizer = WordNetLemmatizer()
        stopWords = set(stopwords.words('english'))
        for punctuation in string.punctuation:
            data = data.replace(punctuation, ' ')
        data = re.split(' ', data)
        data = [word for word in data if word.isalpha()]
        data = [word.lower() for word in data]
        data = [lemmatizer.lemmatize(word) for word in data]
        data = [word for word in data if word not in stopWords]
        return ' '.join(data)
    
    def preapereDataToRec(__self__,breed,filterBy):
        pet_list = __self__.dbSession.query(Pets).all()
        pet_list_filter_by_breed = __self__.dbSession.query(Pets).filter_by(pet_breed=breed)
        if len(pet_list_filter_by_breed.all()) == 0 :
            if(filterBy['pet_lost_location'] and filterBy['pet_gender'] and filterBy['pet_color']):
                pet_list_filter_by_location_color_gender = __self__.dbSession.query(Pets).filter(Pets.pet_lost_location.contains(filterBy['pet_lost_location'])).filter_by(pet_gender=filterBy['pet_gender']).filter_by(pet_color=filterBy['pet_color']).all()
                result = __self__.recomendationDataFrame(pet_list_filter_by_location_color_gender)
                return {'recomendation':result,'filterBy':'location gender and color','list':pet_list_filter_by_location_color_gender}
            elif(filterBy['pet_lost_location'] and filterBy['pet_gender']):
                pet_list_filter_by_location_gender = __self__.dbSession.query(Pets).filter(Pets.pet_lost_location.contains(filterBy['pet_lost_location'])).filter_by(pet_gender=filterBy['pet_gender']).all()
                result = __self__.recomendationDataFrame(pet_list_filter_by_location_gender)
                return {'recomendation':result,'filterBy':'location and gender','list':pet_list_filter_by_location_gender}
            elif(filterBy['pet_lost_location'] and filterBy['pet_color']):
                pet_list_filter_by_location_color = __self__.dbSession.query(Pets).filter(Pets.pet_lost_location.contains(filterBy['pet_lost_location'])).filter_by(pet_color=filterBy['pet_color']).all()
                result = __self__.recomendationDataFrame(pet_list_filter_by_location_color)
                return {'recomendation':result,'filterBy':'location and color','list':pet_list_filter_by_location_color}
            elif(filterBy['pet_color'] and filterBy['pet_gender']):
                pet_list_filter_by_color_gender = __self__.dbSession.query(Pets).filter_by(pet_gender=filterBy['pet_gender']).filter_by(pet_color=filterBy['pet_color']).all()
                result = __self__.recomendationDataFrame(pet_list_filter_by_color_gender)
                return {'recomendation':result,'filterBy':'gender and color','list':pet_list_filter_by_color_gender}
            elif(filterBy['pet_gender']):
                pet_list_filter_by_gender = __self__.dbSession.query(Pets).filter_by(pet_gender=filterBy['pet_gender']).all()
                result = __self__.recomendationDataFrame(pet_list_filter_by_gender)
                return {'recomendation':result,'filterBy':'gender','list':pet_list_filter_by_gender}
            elif(filterBy['pet_color']):
                pet_list_filter_by_color = __self__.dbSession.query(Pets).filter_by(pet_color=filterBy['pet_color']).all()
                result = __self__.recomendationDataFrame(pet_list_filter_by_color)
                return {'recomendation':result,'filterBy':'color','list':pet_list_filter_by_color}
            elif(filterBy['pet_lost_location']):
                pet_list_filter_by_location = __self__.dbSession.query(Pets).filter(Pets.pet_lost_location.contains(filterBy['pet_lost_location'])).all()
                result = __self__.recomendationDataFrame(pet_list_filter_by_location)
                return {'recomendation':result,'filterBy':'location','list':pet_list_filter_by_location}
            else:
                result = __self__.recomendationDataFrame(pet_list)
                return {'recomendation':result,'filterBy':None,'list':pet_list}
        else:
            if(filterBy['pet_lost_location'] and filterBy['pet_gender'] and filterBy['pet_color']):
                pet_list_filter_by_breed_location_color_gender = pet_list_filter_by_breed.filter(Pets.pet_lost_location.contains(filterBy['pet_lost_location'])).filter_by(pet_gender=filterBy['pet_gender']).filter_by(pet_color=filterBy['pet_color']).all()
                if len(pet_list_filter_by_breed_location_color_gender) != 0 :
                    result = __self__.recomendationDataFrame(pet_list_filter_by_breed_location_color_gender)
                    return {'recomendation':result,'filterBy':'breed location gender and color','list':pet_list_filter_by_breed_location_color_gender}
            elif(filterBy['pet_lost_location'] and filterBy['pet_gender']):
                pet_list_filter_by_breed_location_gender = pet_list_filter_by_breed.filter(Pets.pet_lost_location.contains(filterBy['pet_lost_location'])).filter_by(pet_gender=filterBy['pet_gender']).all()
                if len(pet_list_filter_by_breed_location_gender) != 0 :
                    result = __self__.recomendationDataFrame(pet_list_filter_by_breed_location_gender)
                    return {'recomendation':result,'filterBy':'breed location and gender','list':pet_list_filter_by_breed_location_gender}
            elif(filterBy['pet_lost_location'] and filterBy['pet_color']):
                pet_list_filter_by_breed_location_color = pet_list_filter_by_breed.filter(Pets.pet_lost_location.contains(filterBy['pet_lost_location'])).filter_by(pet_color=filterBy['pet_color']).all()
                if len(pet_list_filter_by_breed_location_color) != 0 :
                    result = __self__.recomendationDataFrame(pet_list_filter_by_breed_location_color)
                    return {'recomendation':result,'filterBy':'breed location and color','list':pet_list_filter_by_breed_location_color}
            elif(filterBy['pet_color'] and filterBy['pet_gender']):
                pet_list_filter_by_breed_color_gender = pet_list_filter_by_breed.filter_by(pet_gender=filterBy['pet_gender']).filter_by(pet_color=filterBy['pet_color']).all()
                if len(pet_list_filter_by_breed_color_gender) != 0 :
                    result = __self__.recomendationDataFrame(pet_list_filter_by_breed_color_gender)
                    return {'recomendation':result,'filterBy':'breed color and gender','list':pet_list_filter_by_breed_color_gender}
            elif(filterBy['pet_gender']):
                pet_list_filter_by_breed_gender = pet_list_filter_by_breed.filter_by(pet_gender=filterBy['pet_gender']).all()
                if len(pet_list_filter_by_breed_gender) != 0 :
                    result = __self__.recomendationDataFrame(pet_list_filter_by_breed_gender)
                    return {'recomendation':result,'filterBy':'breed and gender','list':pet_list_filter_by_breed_gender}
            elif(filterBy['pet_color']):
                pet_list_filter_by_breed_color = pet_list_filter_by_breed.filter_by(pet_color=filterBy['pet_color']).all()
                if len(pet_list_filter_by_breed_color) != 0 :
                    result = __self__.recomendationDataFrame(pet_list_filter_by_breed_color)
                    return {'recomendation':result,'filterBy':'color','list':pet_list_filter_by_breed_color}
            elif(filterBy['pet_lost_location']):
                pet_list_filter_by_breed_location = pet_list_filter_by_breed.filter(Pets.pet_lost_location.contains(filterBy['pet_lost_location'])).all()
                if len(pet_list_filter_by_breed_location) == 0 :
                    result = __self__.recomendationDataFrame(pet_list_filter_by_breed)
                    return {'recomendation':result,'filterBy':'breed','list':pet_list_filter_by_breed_location}
                else:
                    result = __self__.recomendationDataFrame(pet_list_filter_by_breed_location)
                    return {'recomendation':result,'filterBy':'breed and location','list':pet_list_filter_by_breed_location}
            else:
                result = __self__.recomendationDataFrame(pet_list_filter_by_breed)
                return {'recomendation':result,'filterBy':'breed','list':pet_list_filter_by_breed}
        
    def recomendationDataFrame(__self__,list):
            date_time = []
            pet_breed = []
            pet_lost_location = []
            pet_name = []
            pet_color = []
            pet_gender = []
            for pet in list:
                date_time.append(pet.date_time.split(','))
                pet_breed.append(pet.pet_breed.split(','))
                pet_lost_location.append(pet.pet_lost_location.split(','))
                pet_name.append(pet.pet_name.split(','))
                pet_color.append(pet.pet_color.split(','))
                pet_gender.append(pet.pet_gender.split(','))
            pet_breed = [__self__.dataCleaning(data) for data in pet_breed]
            pet_lost_location = [__self__.locationCleaning(data) for data in pet_lost_location]
            pet_color = [__self__.dataCleaning(data) for data in pet_color]
            pet_name = [__self__.dataCleaning(data) for data in pet_name]
            pet_gender = [__self__.dataCleaning(data) for data in pet_gender]
            date_time = [__self__.dateTimeCleaning(data) for data in date_time]
            d = {'date_time': date_time, 'pet_breed': pet_breed, 'pet_lost_location': pet_lost_location, 'pet_name': pet_name, 'pet_color': pet_color, 'pet_gender': pet_gender}
            recommendation = pd.DataFrame(data=d)
            recommendation['rec'] = recommendation['date_time'] + ' ' + recommendation['pet_breed'].astype(str) + ' ' + recommendation['pet_lost_location'] + ' ' + recommendation['pet_name'] + ' ' + recommendation['pet_color'] +' ' + recommendation['pet_gender'] 
            return recommendation
    
    def cosineSimiliatray(__self__,filterType,breed,filterBy):
        recomendationResult = __self__.preapereDataToRec(breed,filterBy)
        recomendation = recomendationResult['recomendation']
        recomendation = recomendation.head(len(recomendation))
        countVect = CountVectorizer()
        countMatrix = countVect.fit_transform(recomendation['rec'])
        cosineSim = cosine_similarity(countMatrix, countMatrix)
        indices = pd.Series(recomendation.index, index=recomendation[filterType])
        return {'cosineSim':cosineSim, 'indices':indices,'filterBy':recomendationResult['filterBy'],'list':recomendationResult['list']}
    
    def preapereRecommendPet(__self__,pet_lost_location,pet_breed,pet_name,pet_color,pet_gender):
        pet_list = __self__.dbSession.query(Pets).all()
        if len(pet_list) == 0 :
            message = 'There is no lost or found pet yet.'
            return jsonify({'message':message,'status':'404 NOT FOUND'})
        else:
            if(pet_name):
                obj = __self__.cosineSimiliatray(filterType='pet_name',breed =pet_breed,filterBy={'pet_lost_location' : None,'pet_gender':None,'pet_color':None})
                try:
                    pet_name_cleaning = __self__.inputCleaning(pet_name)
                    idx = obj['indices'][pet_name_cleaning]
                    try:
                        obj = __self__.cosineSimiliatray(filterType='pet_lost_location',breed =pet_breed,filterBy={'pet_lost_location' : None,'pet_gender':None,'pet_color':None})
                        pet_lost_location_cleaning = __self__.inputCleaning(pet_lost_location)
                        idx = obj['indices'][pet_lost_location_cleaning]
                        if(pet_gender and pet_color): # color name loc gender
                            try:
                                result = __self__.recomendationByGenderColorNameLocation(pet_breed,pet_lost_location,pet_name,pet_gender,pet_color)
                                return result
                            except: #gender color loc yok :# color name loc
                                try:
                                    result = __self__.recomendationByGenderNameLocation(pet_breed,pet_lost_location,pet_name,pet_gender)
                                    return result
                                except: #gender color loc yok # loc color a na göre bak 
                                    try:
                                        result = __self__.recomendationByColorNameLocation(pet_breed,pet_lost_location,pet_name,pet_color)
                                        return result
                                    except: # loca göre sırala
                                        result = __self__.recomendationByNameLocation(pet_breed,pet_lost_location,pet_name)
                                        return result
                        elif(pet_color):# color name loc
                            try:
                                result =  __self__.recomendationByColorNameLocation(pet_breed,pet_lost_location,pet_name,pet_color)
                                return result
                            except: # color name loc :# name loc
                                    result = __self__.recomendationByNameLocation(pet_breed,pet_lost_location,pet_name)
                                    return result
                        else: #sadece name ve loc
                            result = __self__.recomendationByNameLocation(pet_breed,pet_lost_location,pet_name)
                            return result
                    except: # loc yok
                        if(pet_gender and pet_color): # color name gender
                            try:
                                result = __self__.recomendationByGenderColorName(pet_breed,pet_name,pet_gender,pet_color)
                                return result
                            except: #gender color loc yok :# color name 
                                try:
                                    result = __self__.recomendationByGenderName(pet_breed,pet_name,pet_gender)
                                    return result
                                except: # color a na göre bak 
                                    try:
                                        result = __self__.recomendationByColorName(pet_breed,pet_name,pet_color)
                                        return result
                                    except: # name göre sırala
                                        result = __self__.recomendationByName(pet_breed,pet_name)
                                        return result
                        elif(pet_color):# color name
                            try:
                                result =  __self__.recomendationByColorName(pet_breed,pet_name,pet_color)
                                return result
                            except: # color name loc :# name
                                result = __self__.recomendationByName(pet_breed,pet_name)
                                return result
                        else: #sadece name 
                            result = __self__.recomendationByName(pet_breed,pet_name)
                            return result
                except: #name i bulamadı loc lanlara bak
                    obj = __self__.cosineSimiliatray(filterType='pet_lost_location',breed =pet_breed,filterBy={'pet_lost_location' : None,'pet_gender':None,'pet_color':None})
                    try:
                        pet_lost_location_cleaning = __self__.inputCleaning(pet_lost_location)
                        idx = obj['indices'][pet_lost_location_cleaning]
                        if(pet_gender and pet_color): # color loc gender
                            try:
                                result = __self__.recomendationByGenderColorLocation(pet_breed,pet_lost_location,pet_gender,pet_color)
                                return result
                            except: # color loc
                                try:
                                    result = __self__.recomendationByGenderLocation(pet_breed,pet_lost_location,pet_gender)
                                    return result
                                except: # loc color a na göre bak 
                                    try:
                                        result = __self__.recomendationByColorLocation(pet_breed,pet_lost_location,pet_color)
                                        return result
                                    except: # loca göre sırala
                                        result = __self__.recomendationByLocation(pet_breed,pet_lost_location)
                                        return result
                        elif(pet_color):# color loc
                            try:
                                result =  __self__.recomendationByColorLocation(pet_breed,pet_lost_location,pet_color)
                                return result
                            except: # loc
                                result = __self__.recomendationByLocation(pet_breed,pet_lost_location)
                                return result
                        else: #sadece loc
                            result = __self__.recomendationByLocation(pet_breed,pet_lost_location)
                            return result
                    except: #loc da yok 
                        message = 'Opps sorry we cannot recommend like this pet. You can new alert for the lost.'
                        return jsonify({'message':message,'status':'404 NOT FOUND'})
            else:#name girmemiş
                obj = __self__.cosineSimiliatray(filterType='pet_lost_location',breed =pet_breed,filterBy={'pet_lost_location' : None,'pet_gender':None,'pet_color':None})
                try:
                    pet_lost_location_cleaning = __self__.inputCleaning(pet_lost_location)
                    idx = obj['indices'][pet_lost_location_cleaning]
                    if(pet_gender and pet_color): # color loc gender
                        try:
                            result = __self__.recomendationByGenderColorLocation(pet_breed,pet_lost_location,pet_gender,pet_color)
                            return result
                        except: # color loc
                            try:
                                result = __self__.recomendationByGenderLocation(pet_breed,pet_lost_location,pet_gender)
                                return result
                            except: # loc color a na göre bak 
                                try:
                                    result = __self__.recomendationByColorLocation(pet_breed,pet_lost_location,pet_color)
                                    return result
                                except: # loca göre sırala
                                    result = __self__.recomendationByLocation(pet_breed,pet_lost_location)
                                    return result
                    elif(pet_color):# color loc
                        try:
                            result =  __self__.recomendationByColorLocation(pet_breed,pet_lost_location,pet_color)
                            return result
                        except: # loc
                            result = __self__.recomendationByLocation(pet_breed,pet_lost_location)
                            return result
                    else: #sadece loc
                        result = __self__.recomendationByLocation(pet_breed,pet_lost_location)
                        return result
                except:
                    message = 'Opps sorry we cannot recommend like this pet. You can new alert for the lost.'
                    return jsonify({'message':message,'status':'404 NOT FOUND'})

    def recomendationByGenderColorNameLocation(__self__,pet_breed,pet_lost_location,pet_name,pet_gender,pet_color):
        pet_lost_location_cleaning = __self__.inputCleaning(pet_lost_location)
        obj = __self__.cosineSimiliatray(filterType='pet_name',breed =pet_breed,filterBy={'pet_lost_location' :  pet_lost_location_cleaning.split(' ')[1],'pet_gender':pet_gender,'pet_color':pet_color})
        pet_name_cleaning = __self__.inputCleaning(pet_name)
        idx = obj['indices'][pet_name_cleaning]
        return __self__.checkLenidX(obj,idx)
    def recomendationByGenderNameLocation(__self__,pet_breed,pet_lost_location,pet_name,pet_gender):
        pet_lost_location_cleaning = __self__.inputCleaning(pet_lost_location)
        obj = __self__.cosineSimiliatray(filterType='pet_name',breed =pet_breed,filterBy={'pet_lost_location' :  pet_lost_location_cleaning.split(' ')[1],'pet_gender':pet_gender,'pet_color':None})
        pet_name_cleaning = __self__.inputCleaning(pet_name)
        idx = obj['indices'][pet_name_cleaning]
        return __self__.checkLenidX(obj,idx)
    def recomendationByColorNameLocation(__self__,pet_breed,pet_lost_location,pet_name,pet_color):
        pet_lost_location_cleaning = __self__.inputCleaning(pet_lost_location)
        obj = __self__.cosineSimiliatray(filterType='pet_name',breed =pet_breed,filterBy={'pet_lost_location' :  pet_lost_location_cleaning.split(' ')[1],'pet_gender':None,'pet_color':pet_color})
        pet_name_cleaning = __self__.inputCleaning(pet_name)
        idx = obj['indices'][pet_name_cleaning]
        return __self__.checkLenidX(obj,idx)
    def recomendationByNameLocation(__self__,pet_breed,pet_lost_location,pet_name):
        pet_lost_location_cleaning = __self__.inputCleaning(pet_lost_location)
        obj = __self__.cosineSimiliatray(filterType='pet_name',breed =pet_breed,filterBy={'pet_lost_location' :  pet_lost_location_cleaning.split(' ')[1],'pet_gender':None,'pet_color':None})
        pet_name_cleaning = __self__.inputCleaning(pet_name)
        idx = obj['indices'][pet_name_cleaning]
        return __self__.checkLenidX(obj,idx)

    def recomendationByGenderColorLocation(__self__,pet_breed,pet_lost_location,pet_gender,pet_color):
        pet_lost_location_cleaning = __self__.inputCleaning(pet_lost_location)
        obj = __self__.cosineSimiliatray(filterType='pet_lost_location',breed =pet_breed,filterBy={'pet_lost_location' :  pet_lost_location_cleaning.split(' ')[1],'pet_gender':pet_gender,'pet_color':pet_color})
        idx = obj['indices'][pet_lost_location_cleaning]
        return __self__.checkLenidX(obj,idx)
    def recomendationByGenderLocation(__self__,pet_breed,pet_lost_location,pet_gender):
        pet_lost_location_cleaning = __self__.inputCleaning(pet_lost_location)
        obj = __self__.cosineSimiliatray(filterType='pet_lost_location',breed =pet_breed,filterBy={'pet_lost_location' :  pet_lost_location_cleaning.split(' ')[1],'pet_gender':pet_gender,'pet_color':None})
        idx = obj['indices'][pet_lost_location_cleaning]
        return __self__.checkLenidX(obj,idx)
    def recomendationByColorLocation(__self__,pet_breed,pet_lost_location,pet_color):
        pet_lost_location_cleaning = __self__.inputCleaning(pet_lost_location)
        obj = __self__.cosineSimiliatray(filterType='pet_lost_location',breed =pet_breed,filterBy={'pet_lost_location' :  pet_lost_location_cleaning.split(' ')[1],'pet_gender':None,'pet_color':pet_color})
        idx = obj['indices'][pet_lost_location_cleaning]
        return __self__.checkLenidX(obj,idx)
    def recomendationByLocation(__self__,pet_breed,pet_lost_location):
        pet_lost_location_cleaning = __self__.inputCleaning(pet_lost_location)
        obj = __self__.cosineSimiliatray(filterType='pet_lost_location',breed =pet_breed,filterBy={'pet_lost_location' :  pet_lost_location_cleaning.split(' ')[1],'pet_gender':None,'pet_color':None})
        idx = obj['indices'][pet_lost_location_cleaning]
        return __self__.checkLenidX(obj,idx)
    
    def recomendationByGenderColorName(__self__,pet_breed,pet_name,pet_gender,pet_color):
        obj = __self__.cosineSimiliatray(filterType='pet_name',breed =pet_breed,filterBy={'pet_lost_location' : None,'pet_gender':pet_gender,'pet_color':pet_color})
        pet_name_cleaning = __self__.inputCleaning(pet_name)
        idx = obj['indices'][pet_name_cleaning]
        return __self__.checkLenidX(obj,idx)
    def recomendationByGenderName(__self__,pet_breed,pet_name,pet_gender):
        obj = __self__.cosineSimiliatray(filterType='pet_name',breed =pet_breed,filterBy={'pet_lost_location' : None,'pet_gender':pet_gender,'pet_color':None})
        pet_name_cleaning = __self__.inputCleaning(pet_name)
        idx = obj['indices'][pet_name_cleaning]
        return __self__.checkLenidX(obj,idx)
    def recomendationByColorName(__self__,pet_breed,pet_name,pet_color):
        obj = __self__.cosineSimiliatray(filterType='pet_name',breed =pet_breed,filterBy={'pet_lost_location' : None,'pet_gender':None,'pet_color':pet_color})
        pet_name_cleaning = __self__.inputCleaning(pet_name)
        idx = obj['indices'][pet_name_cleaning]
        return __self__.checkLenidX(obj,idx)
    def recomendationByName(__self__,pet_breed,pet_name):
        obj = __self__.cosineSimiliatray(filterType='pet_name',breed =pet_breed,filterBy={'pet_lost_location' : None,'pet_gender':None,'pet_color':None})
        pet_name_cleaning = __self__.inputCleaning(pet_name)
        idx = obj['indices'][pet_name_cleaning]
        return __self__.checkLenidX(obj,idx)
    
    def checkLenidX(__self__,obj,idx):
        try:
            if len(idx) > 0:
                result = __self__.recommendationResult(obj,obj['list'],idx[0])
                return result
        except:
            result = __self__.recommendationResult(obj,obj['list'],idx)
            return result

    def recommendationResult(__self__,obj,pet_list,idx):
        sim_scores_without_sorted = list(enumerate(obj['cosineSim'][idx]))
        sim_scores = sorted(sim_scores_without_sorted, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[0:30]
        petindices = [i[0] for i in sim_scores]
        recommendation = pd.DataFrame(columns=["pet_id","record_type", "date_time","pet_name","pet_breed","pet_color","pet_age","pet_gender","pet_image","pet_lost_location"])
        count = 0
        for i in petindices:
            for index, pet in enumerate(pet_list):
                    if(index == i):
                        recommendation.at[count, "pet_id"] = pet.pet_id
                        recommendation.at[count, "record_type"] = pet.record_type
                        recommendation.at[count, "date_time"] = pet.date_time
                        recommendation.at[count, "pet_name"] = pet.pet_name
                        recommendation.at[count, "pet_breed"] = pet.pet_breed
                        recommendation.at[count, "pet_color"] = pet.pet_color
                        recommendation.at[count, "pet_age"] = pet.pet_age
                        recommendation.at[count, "pet_gender"] = pet.pet_gender
                        recommendation.at[count, "pet_image"] = pet.pet_image
                        recommendation.at[count, "pet_lost_location"] = pet.pet_lost_location
                        recommendation.at[count, "score"] = f"{sim_scores_without_sorted[i]}"
                        count += 1
        return recommendation        

    
    def recommendPet(__self__,record_type,date_time,pet_name,pet_breed,pet_color,pet_age,pet_gender,pet_image,pet_details,pet_lost_location,created_id):
        recomendation = __self__.preapereRecommendPet(pet_lost_location,pet_breed,pet_name,pet_color,pet_gender)
        json_data = recomendation.to_json(orient="records")
        json_load = json.loads(json_data)
        response = json.dumps(json_load)
        return response    

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
    