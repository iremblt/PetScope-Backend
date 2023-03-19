
import nltk
import string
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import pandas as pd

def createMostRecomendationDataFrame(scores):
    lost_pets = pd.read_csv('Lost__found__adoptable_pets.csv')
    most_simalitiaries = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    most_simalitiaries_data_frame= pd.DataFrame(columns=["Animal_ID", "Record_Type", "Current_Location", "Animal_Name","animal_type","Age",
    "Animal_Gender","Animal_Breed","Animal_Color","Date","Obfuscated_Address","City","State","Zip","obfuscated_latitude",
    "obfuscated_longitude","Image","image_alt_text","Other"])
    count = 0
    for i in most_simalitiaries:
        most_simalitiaries_data_frame.at[count, "Animal_ID"] = lost_pets["Animal_ID"][i]
        most_simalitiaries_data_frame.at[count, "Record_Type"] = lost_pets["Record_Type"][i]
        most_simalitiaries_data_frame.at[count, "Current_Location"] = lost_pets["Current_Location"][i]
        most_simalitiaries_data_frame.at[count, "Animal_Name"] = lost_pets["Animal_Name"][i]
        most_simalitiaries_data_frame.at[count, "animal_type"] = lost_pets["animal_type"][i]
        most_simalitiaries_data_frame.at[count, "Age"] = lost_pets["Age"][i]
        most_simalitiaries_data_frame.at[count, "Animal_Gender"] = lost_pets["Animal_Gender"][i]
        most_simalitiaries_data_frame.at[count, "Animal_Breed"] = lost_pets["Animal_Breed"][i]
        most_simalitiaries_data_frame.at[count, "Animal_Color"] = lost_pets["Animal_Color"][i]
        most_simalitiaries_data_frame.at[count, "Date"] = lost_pets["Date"][i]
        most_simalitiaries_data_frame.at[count, "Obfuscated_Address"] = lost_pets["Obfuscated_Address"][i]
        most_simalitiaries_data_frame.at[count, "City"] = lost_pets["City"][i]
        most_simalitiaries_data_frame.at[count, "State"] = lost_pets["State"][i]
        most_simalitiaries_data_frame.at[count, "Zip"] = lost_pets["Zip"][i]
        most_simalitiaries_data_frame.at[count, "obfuscated_latitude"] = lost_pets["obfuscated_latitude"][i]
        most_simalitiaries_data_frame.at[count, "obfuscated_longitude"] = lost_pets["obfuscated_longitude"][i]
        most_simalitiaries_data_frame.at[count, "Image"] = lost_pets["Image"][i]
        most_simalitiaries_data_frame.at[count, "image_alt_text"] = lost_pets["image_alt_text"][i]
        most_simalitiaries_data_frame.at[count, "Other"] = lost_pets["Other"][i]
        most_simalitiaries_data_frame.at[count, "score"] = f"{scores[i]}"
        count += 1
    return most_simalitiaries_data_frame

def recommendation_pet(tags):
    model = Word2Vec.load("models/model_cbow.bin")
    model.init_sims(replace=True)
    lost_pets = pd.read_csv('Lost__found__adoptable_pets.csv')
    lost_pets["tags"] = lost_pets.tags.apply(tags_edit)
    corpus = get_and_sort_corpus(data)
    tfidf_vec_tr = TfidfEmbeddingVectorizer(model)
    tfidf_vec_tr.fit(corpus)
    doc_vec = tfidf_vec_tr.transform(corpus)
    doc_vec = [doc.reshape(1, -1) for doc in doc_vec]
    assert len(doc_vec) == len(corpus)
    input = tags
    input = input.split(",")
    input = ingredient_parser(input)
    input_embedding = tfidf_vec_tr.transform([input])[0].reshape(1, -1)
    cos_sim = map(lambda x: cosine_similarity(input_embedding, x)[0][0], doc_vec)
    scores = list(cos_sim)
    recommendations = createMostRecomendationDataFrame(scores)
    return recommendations


def tags_edit(tags):
    common_words = ['fresh', 'oil', 'a', 'red', 'bunch', ...]
    if isinstance(tags, list):
        tags = tags
    else:
        tags = list(tags.split(" "))
    translator = str.maketrans('', '', string.punctuation)
    lemmatizer = WordNetLemmatizer()
    tag_list = []
    for i in tags:
        i.translate(translator)
        items = re.split(' |-', i)
        items = [word for word in items if word.isalpha()]
        items = [word.lower() for word in items]
        # remove accents
        items = [unidecode.unidecode(word) for word in items]
        # Lemmatize words so we can compare words to measuring words
        items = [lemmatizer.lemmatize(word) for word in items]
        # get rid of stop words
        stop_words = set(corpus.stopwords.words('english'))
        items = [word for word in items if word not in stop_words]
        # Gets rid of measuring words/phrases, e.g. heaped teaspoon
        items = [word for word in items if word not in measures]
        # Get rid of common easy words
        items = [word for word in items if word not in words_to_remove]
        if items:
            ingred_list.append(' '.join(items))
    return ingred_list