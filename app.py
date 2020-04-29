from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from db_schema import Weed, DB, migrate
import os 
import pandas as pd
import pickle
from sqlite_connection import df_create
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

app = Flask(__name__)


# # # Load the model from file 
nn_model = joblib.load('pickled_files/nn_model.pkl')  
tfidf = joblib.load('pickled_files/tfidf.pkl')  

# #Load the dataframe from file
df = pd.read_pickle("pickled_files/df.pkl")


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
    import joblib
    _, similar_topic_indices = nn_model.kneighbors(query.todense())
    indices = similar_topic_indices[0]
    # print(indices)
    recc_values = {
    'first': {},
    'second': {},
    'third': {},
    'fourth': {},
    'fifth': {}
    }
    
    def get_index_values(index):
        output_values = {
        'Strain':[], 
        'Type':[], 
        'Rating':[], 
        'Flavor':[], 
        'Effects':[], 
        'Description':[]}

        for value in output_values:
            output_values[value].append(dframe[value][index])
        return output_values

    for key, value in enumerate(recc_values):
        recc_values[value] = get_index_values(indices[key])
    return recc_values

def predict(user_inputs):
    """
    Takes a users perferences/symptoms are uses a prediction model to 
    return the best cannabis strains for that user. 
    """
    strain_query = get_user_inputs(user_inputs)
    reccomondations = output_user_reccomendations(strain_query, df)
    return reccomondations

@app.route("/recommendations")
def reccomend():
    # user_inputs = request.get_json(force=True)
    user_inputs = {
        'effects': ['happy', 'creative'],
        'flavors': ['strawberry, pineapple'],
        'ailments': ['depression', 'headaches']
    }
    prediction = predict(user_inputs)
    return jsonify(prediction)


def create_app():
    """ Create and configure flask app"""
    app = Flask(__name__)
    
    # configure the database:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cannabis.sqlite3'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # suppress warning messages
    
    DB.init_app(app)
    migrate.init_app(app, DB)

    return app


@app.route('/')
def root():
    return "We have the best app"


# route to display all strains if we want to 
@app.route("/strains")
def strains():
    """
    Function: returns a list of all the cannbais strains.
    Returns: list of strains as a JSON array
    """
    try:
        all_strains = df.to_json(orient="records")
    except Exception as e:
        raise e

    return(all_strains)