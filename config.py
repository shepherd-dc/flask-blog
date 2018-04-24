import os
SECRET_KEY = os.urandom(24)

DEBUG = True

# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = ''
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'flask_blog'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
