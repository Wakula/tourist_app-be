from helper_classes.application_blueprint import ApplicationBlueprint
from .urls import urls
from .controllers import controllers
from .models import models

app = ApplicationBlueprint('trip', __name__, controllers, urls, models)
