import sqlite3 
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


CSV_FILEPATH = os.path.join(os.path.dirname(__file__), "cannabis.csv")
data = pd.read_csv(CSV_FILEPATH)


def df_create(CSV_FILEPATH):
    df = pd.read_csv(CSV_FILEPATH)
    # Replace / and spaces in column names with underscores
    df.columns = df.columns.str.replace('/', "_")
    df.columns = df.columns.str.replace(' ', '_')
    return df


cannabis_df = df_create('cannabis.csv')
conn = sqlite3.connect('cannabis.sqlite3')
cannabis_df.to_sql('cannabis', conn, if_exists='replace', index=False)
curs = conn.cursor()
conn.commit()

# print("-------")
# query = """
# SELECT Strain  
# FROM Cannabis 
# """
# curs.execute(query)
# print(curs.fetchall())

conn.commit()
