from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()



class Conexion(): 
    PG_USER=os.getenv('PG_USER')
    PG_PASSWORD=os.getenv('PG_PASSWORD')
    PG_HOST=os.getenv('PG_HOST')
    PG_DATABASE=os.getenv('PG_DATABASE') 
    PG_PORT=os.getenv('PG_PORT')

    def __init__(self):
             self. url=f"postgresql+psycopg2://{self.PG_USER}:{self.PG_PASSWORD}@{self.PG_HOST}/{self.PG_DATABASE}"
             self.engine=create_engine(self.url)
    
       
    
    def get_conexion(self, engine, base):
        self.base=base.metadata.create_all(engine) 
        self.Session=sessionmaker(bind=engine) 
        self.session=self.Session() 
        return self.session
    
    def get_engine(self): 
        return self.engine
    
    def get_Session(self): 
         return self.session
 
        
        


