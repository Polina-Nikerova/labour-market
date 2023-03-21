import sqlalchemy
from sqlalchemy import MetaData, String, Integer, Float, Column, DateTime, Text
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, scoped_session
import pandas as pd
from models import session, Vacancy, Base_vacancy, connection, engine
from preprocessing import load_data
import pymongo as pym
from bson import ObjectId

def get_data_from_mongodb(table_name):
    client = pym.MongoClient("mongodb://localhost:27017/")
    mydatabase = client['labour_market']  # create database
    mycollection = mydatabase[table_name]
    cursor = mycollection.find()
    final_records = [i for i in cursor]
    final_records = final_records[0]
    ids = final_records['_id']
    del final_records['_id']
    return ids, final_records
def insert_mongo_db(record, table_name):
    client = pym.MongoClient("mongodb://localhost:27017/")
    mydatabase = client['labour_market']  # create database
    mycollection = mydatabase[table_name]
    ids, data = get_data_from_mongodb(table_name)
    mycollection.delete_one({'_id': ObjectId(ids)})
    for key, value in data.items():
        for key1, value1 in record.items():
            if key == key1:
                for key2, value2 in value.items():
                    freq = record[key1][key2]
                    freq1 = data[key][key2]
                    if freq == None:
                        freq = 0
                    if freq1 == None:
                        freq1 = 0
                    data[key][key2] = freq + freq1
    mycollection.insert_one(data)
    print('Insert data in MongoDB')
def insert_base_table(vacancy_name, salary_from, salary_to, job_description, skills):
    add_row = Base_vacancy(
        vacancy_name=vacancy_name,
        salary_from=salary_from,
        salary_to=salary_to,
        job_description=job_description,
        skills=skills
    )
    session.add(add_row)
    session.commit()
    print('add rows')

def insert_vacancy_table(df):
    df['skills'] = df['skills'].apply(lambda x: x.replace('[', '').replace(']', ''))
    for index, row in df.iterrows():
        add_row = Vacancy(
            vacancy_name=row[1],
            salary_from=row[2],
            salary_to=row[3],
            job_description=row[4],
            skills=row[5],
            vacancy_category=row[6]
        )
        session.add(add_row)
        session.commit()
        print('add row')

#example: inserting data from excel file
def insert_table():
    df = load_data('df_test')
    df['Skills'] = df['Skills'].apply(lambda x: x.replace('[', '').replace(']', ''))
    for index, row in df.iterrows():
        add_row = Vacancy(
            vacancy_name=row[1],
            salary_from=row[2],
            salary_to=row[3],
            job_description=row[4],
            skills=row[5],
            vacancy_category=row[6]
        )
        session.add(add_row)
        session.commit()
        print('add row')

def get_data_query():
    query = text('SELECT * FROM base_vacancy')
    result = connection.execute(query).fetchall()
    df = pd.DataFrame(result)
    return df

def get_vacancy_data():
    query = text('SELECT * FROM vacancy')
    result = connection.execute(query).fetchall()
    df = pd.DataFrame(result)
    return df