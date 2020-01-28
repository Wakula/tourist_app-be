from helper_classes.base_view import BaseView
from flask import current_app, request, g
from helper_classes.auth_decorator import otc_authorization


class OtcView(BaseView):
    @otc_authorization
    def patch(self, uuid):
        data, status = current_app.blueprints['otc'].controllers\
            .OtcController.handle_uuid(uuid)
        return self._get_response(data, status_code=status)
