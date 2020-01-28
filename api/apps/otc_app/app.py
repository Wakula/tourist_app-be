from helper_classes.application_blueprint import ApplicationBlueprint
from .urls import urls
from .controllers import controllers

app = ApplicationBlueprint('otc', __name__, controllers, urls)
