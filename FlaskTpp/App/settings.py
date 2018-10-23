import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_db_uri(dbinfo):

    engine = dbinfo.get("ENGINE")
    driver = dbinfo.get("DRIVER")
    user = dbinfo.get("USER")
    password = dbinfo.get("PASSWORD")
    host = dbinfo.get("HOST")
    port = dbinfo.get("PORT")
    name = dbinfo.get("NAME")

    return "{}+{}://{}:{}@{}:{}/{}".format(engine, driver, user, password, host, port, name)


class Config:

    TESTING = False

    DEBUG = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "Rock"

    SESSION_TYPE = "redis"

    SESSION_COOKIE_SECURE = True

    SESSION_USE_SIGNER = True


class DevelopConfig(Config):

    DEBUG = True

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "sunck1999",
        "HOST": "localhost",
        "PORT": 3306,
        "NAME": "GP1FlaskTpp"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class TestingConfig(Config):

    TESTINE = True

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "sunck1999",
        "HOST": "localhost",
        "PORT": 3306,
        "NAME": "GP1FlaskDay02"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class StagingConfig(Config):

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "sunck1999",
        "HOST": "localhost",
        "PORT": 3306,
        "NAME": "GP1FlaskDay02"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


class ProductConfig(Config):

    dbinfo = {
        "ENGINE": "mysql",
        "DRIVER": "pymysql",
        "USER": "root",
        "PASSWORD": "sunck1999",
        "HOST": "localhost",
        "PORT": 3306,
        "NAME": "GP1FlaskDay02"
    }

    SQLALCHEMY_DATABASE_URI = get_db_uri(dbinfo)


envs = {
    "develop": DevelopConfig,
    "testing": TestingConfig,
    "staging": StagingConfig,
    "product": ProductConfig,
    "default": DevelopConfig
}

ADMINS = ["Zahir", "root"]

FILE_PATH_PREFIX = "/static/uploads/icons"
UPLOAD_DIR = os.path.join(BASE_DIR, "App/static/uploads/icons")