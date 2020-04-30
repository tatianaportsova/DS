from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import os 
import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

HEROKU_BUILDPACK_GIT_LFS_REPO = "https://github.com/Build-Week-Medicine-Cabinet/DS/tree/master/pickled_files"

app = Flask(__name__)

# creates the flask app and configures it. 
def create_app():
    """ Create and configure flask app"""
    app = Flask(__name__)
    CORS(app)

    # configure the database:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cannabis.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # suppress warning messages
    DB = SQLAlchemy(app)

    return app


@app.route('/')
def root():
    return "We have the best app"


# # # Load the model from file 
nn_model = joblib.load("pickled_files/nn_3.pkl")  
tfidf = joblib.load("pickled_files/tfidf_pickled.pkl")  

# #Load the dataframe from file
dfcleaned = joblib.load("pickled_files/tokens_pickled.pkl")


## GOING TO NEED TO CREATE A FUNCTION TO PARSE
## THE JSON DICTIONARY SENT TO US TO MATCH THE BELOW 
## PYTHON DICTIONARY.

def get_user_inputs(data):
        import joblib 
        user_desc = ''
        for index in data:
            for values in data[index]:
                user_desc += '\n' + values
        return tfidf.transform([user_desc])


def output_user_reccomendations(query, dframe):
    _, similar_topic_indices = nn_model.kneighbors(query.todense())
    indices = list(similar_topic_indices[0])
    recc_values = []
    
    def get_index_values(index):
        output_values = {
        'ID':[],
        'Strain':[], 
        'Type':[], 
        'Rating':[], 
        'Flavor':[], 
        'Effects':[], 
        'Description':[]}
        output_values['Strain'].append(dframe['Strain'][index])

        return output_values['Strain'][0]
    for key in range(0, len(indices)):
        recc_values.append(get_index_values(indices[key]))
    return recc_values


def predict(user_inputs):
    """
    Takes a users perferences/symptoms are uses a prediction model to 
    return the best cannabis strains for that user. 
    """
    strain_query = get_user_inputs(user_inputs)
    reccomondations = output_user_reccomendations(strain_query, dfcleaned)
    return reccomondations

@app.route("/recommendations", methods=["GET"])
def recommend():
    # parse input features from request
    # request_json = request.get_json()
    # user_inputs = request_json['input']
    # user_inputs = request.get_json(force=True)
    user_inputs = {
        'effects': ['happy', 'creative'],
        'flavors': ['strawberry, pineapple'],
        'ailments': ['depression', 'headaches']
    }
    prediction = predict(user_inputs)
    response = json.dumps(prediction)
    return response


# optional route to display all strains if we want to 
# @app.route("/strains")
# def strains():
#     """
#     Function: returns a list of all the cannbais strains.
#     Returns: list of strains as a JSON array
#     """
#     try:
#         all_strains = df.to_json(orient="records")
#     except Exception as e:
#         raise e

#     return(all_strains)
