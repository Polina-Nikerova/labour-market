from sqlalchemy import MetaData, String, Integer, Float, Column, DateTime, Text
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker, scoped_session
import pandas as pd
import sqlalchemy as db

#create_engine(DB_PATH, echo=False, poolclass=StaticPool, connect_args={'check_same_thread': False})
engine = db.create_engine('sqlite:///test.db')
connection = engine.connect()
session = scoped_session(
            sessionmaker(
                autoflush=True,
                autocommit=False,
                bind=engine
            )
        )
metadata = MetaData()
Base = declarative_base()

class Base_vacancy(Base):
    __tablename__ = 'base_vacancy'
    id = Column(Integer, primary_key=True)
    vacancy_name = Column(String(150))
    salary_from = Column(Integer)
    salary_to = Column(Integer)
    job_description = Column(Text)
    skills = Column(Text)
class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True)
    vacancy_name = Column(String(150))
    salary_from = Column(Integer)
    salary_to = Column(Integer)
    job_description = Column(Text)
    skills = Column(Text)
    vacancy_category = Column(String(150))

#Base.metadata.drop_all(bind=engine, tables=[Vacancy.__table__])
#Base.metadata.create_all(engine)

#df = pd.read_excel('./files/df_test.xlsx')
#df['Skills'] = df['Skills'].apply(lambda x: x.replace('[', '').replace(']', ''))
#for index, row in df.iterrows():
    #print(tuple(row))
    #add_row = Vacancy(
     #   vacancy_name=row[1],
     #   salary_from=row[2],
     #   salary_to=row[3],
     #   job_description=row[4],
     #   skills=row[5],
      #  vacancy_category=row[6]
   # )
   # session.add(add_row)
   # session.commit()
   # print('add row')