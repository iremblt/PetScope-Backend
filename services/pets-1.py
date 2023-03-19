from flask import jsonify
import pandas as pd
from models.pets import petSchema
import json
import random 

class pets():
    pet_schemas = petSchema(many=True)
    lost_pets = pd.read_csv('Lost__found__adoptable_pets.csv')

    def getPetList(_self_):
        lost_pets = pd.read_csv('Lost__found__adoptable_pets.csv')
        list = _self_.createJsonFile(lost_pets)
        return list

    def getPetByID(_self_, id):
        lost_pets = pd.read_csv('Lost__found__adoptable_pets.csv')
        index = lost_pets.index[lost_pets['Animal_ID'] == id].tolist(
        )
        if len(index):
            list = _self_.createJsonFile(lost_pets)
            return list[index[0]]
        else:
            message = 'There is no pet for this animal id. Check your animal id!'
            return jsonify({'message': message, 'success': '404 NOT FOUND'})
    
    def deletePet(_self_,id): 
        lost_pets = pd.read_csv('Lost__found__adoptable_pets.csv')
        list = _self_.createJsonFile(lost_pets)
        index = lost_pets.index[lost_pets['Animal_ID'] == id].tolist()       
        if len(index) :
            pet_list = lost_pets.drop(index[0])
            pet = list[index[0]]
            pet_list.to_csv('Lost__found__adoptable_pets.csv', index=False)
            list = _self_.createJsonFile(pet_list)
            return pet
        else:
            message = 'There is no pet for this animal id. Check your animal id!'
            return jsonify({'message': message, 'success': '404 NOT FOUND'})

    def addPet(_self_,Record_Type,Current_Location,Animal_Name,animal_type,Age,Animal_Gender,Animal_Breed,Animal_Color,Date,Obfuscated_Address,City,State,Zip,obfuscated_latitude,obfuscated_longitude,Image,image_alt_text,Other):
        AnimalID = _self_.createAnimalID(len(_self_.lost_pets))
        data = {'Animal_ID': [AnimalID],'Record_Type': [Record_Type],
        'Current_Location': [Current_Location],'Animal_Name': [Animal_Name],'animal_type': [animal_type],
        'Age': [Age],'Animal_Gender': [Animal_Gender],'Animal_Breed': [Animal_Breed],'Animal_Color': [Animal_Color],
        'Date': [Date],'Obfuscated_Address': [Obfuscated_Address],'City': [City],'State': [State],'Zip': [Zip],
        'obfuscated_latitude': [obfuscated_latitude],'obfuscated_longitude': [obfuscated_longitude],'Image': [Image],
        'image_alt_text': [image_alt_text],'Other': [Other]
        }
        df = pd.DataFrame(data)
        df.to_csv('Lost__found__adoptable_pets.csv', mode='a', index=False, header=False)
        lost_pets = pd.read_csv('Lost__found__adoptable_pets.csv')
        list = _self_.createJsonFile(lost_pets)
        index = lost_pets.index[lost_pets['Animal_ID'] == AnimalID].tolist()
        pet = list[index[0]]
        return pet

    def editPet(_self_,id,Record_Type,Current_Location,Animal_Name,animal_type,Age,Animal_Gender,Animal_Breed,Animal_Color,Date,Obfuscated_Address,City,State,Zip,obfuscated_latitude,obfuscated_longitude,Image,image_alt_text,Other):
        lost_pets = pd.read_csv('Lost__found__adoptable_pets.csv')
        index = lost_pets.index[lost_pets['Animal_ID'] == id].tolist()
        if len(index):
            lost_pets.loc[index[0], 'Record_Type'] = Record_Type
            lost_pets.loc[index[0], 'Current_Location'] = Current_Location
            lost_pets.loc[index[0], 'Animal_Name'] = Animal_Name
            lost_pets.loc[index[0], 'animal_type'] = animal_type
            lost_pets.loc[index[0], 'Age'] = Age
            lost_pets.loc[index[0], 'Animal_Gender'] = Animal_Gender
            lost_pets.loc[index[0], 'Animal_Breed'] = Animal_Breed
            lost_pets.loc[index[0], 'Animal_Color'] = Animal_Color
            lost_pets.loc[index[0], 'Date'] = Date
            lost_pets.loc[index[0], 'Obfuscated_Address'] = Obfuscated_Address
            lost_pets.loc[index[0], 'City'] = City
            lost_pets.loc[index[0], 'State'] = State
            lost_pets.loc[index[0], 'Zip'] = Zip
            lost_pets.loc[index[0], 'obfuscated_latitude'] = obfuscated_latitude
            lost_pets.loc[index[0], 'obfuscated_longitude'] = obfuscated_longitude
            lost_pets.loc[index[0], 'Image'] = Image
            lost_pets.loc[index[0], 'image_alt_text'] = image_alt_text
            lost_pets.loc[index[0], 'Other'] = Other
            lost_pets.to_csv('Lost__found__adoptable_pets.csv', index=False)
            list = _self_.createJsonFile(lost_pets)
            pet = list[index[0]]
            return pet
        else:
            message = 'There is no pet for this animal id. Check your animal id!'
            return jsonify({'message': message, 'success': '404 NOT FOUND'})
    
    def recomendation(_self_, id):
        lost_pets = pd.read_csv('Lost__found__adoptable_pets.csv')
        index = lost_pets.index[lost_pets['Animal_ID'] == id].tolist(
        )
        if len(index):
            list = _self_.createJsonFile(lost_pets)
            return list[index[0]]
        else:
            message = 'There is no pet for this animal id. Check your animal id!'
            return jsonify({'message': message, 'success': '404 NOT FOUND'})
        
    def getRandomNumber(_self_,lengthOfList):
        if lengthOfList < 1000000:
            return 'A' + str(random.randint(100000,1000000))
        else:
            return 'A' + str(random.randint(100000,10000000))

    def createAnimalID(_self_,lengthOfList):
        randomId = _self_.getRandomNumber(lengthOfList)
        index = _self_.lost_pets.index[_self_.lost_pets['Animal_ID'] == randomId].tolist()
        if len(index) > 0 :
            return _self_.createAnimalID(lengthOfList)
        else:
            return randomId
    
    def createJsonFile(_self_,file):
        file.to_json(
            'Lost__found__adoptable_pets.json', orient='records')
        jsonFile = open('Lost__found__adoptable_pets.json')
        list = json.load(jsonFile)
        return list
    