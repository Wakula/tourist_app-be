from flask_sqlalchemy import SQLAlchemy
from helper_classes.model_registry import ModelRegistry
db = SQLAlchemy()


def set_db(main_app):
    model_registrator = ModelRegistry()
    setattr(main_app, "models", model_registrator)
    db.init_app(main_app)
    setattr(main_app, "db", db)