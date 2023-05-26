from pydantic import BaseSettings

class Setting(BaseSettings):
    database_hostname:str
    database_name:str
    database_username:str
    database_password:str
    database_port:str
    secret_key:str
    algorithm:str
    access_token_expire_time:int
    
    class Config:
        env_file = ".env"

settings = Setting()        