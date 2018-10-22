# from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
# from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
db = SQLAlchemy()
migrate = Migrate()

cache = Cache(
    config={
        "CACHE_TYPE": "redis"
    }
)


def init_ext(app):
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    # Session(app)
    # Bootstrap(app)