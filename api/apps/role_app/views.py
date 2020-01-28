from helper_classes.base_view import BaseView
from flask import current_app, request, g
from marshmallow import ValidationError
from helper_classes.auth_decorator import login_required
from .schemas.role_schema import RoleSchema


class RoleView(BaseView):
    def __init__(self):
        self.role_controller = current_app.blueprints['role'].controllers.RoleController


    @login_required
    def post(self):
        try:
            role_data = RoleSchema().load(request.json)
        except (ValidationError, Exception) as err:
            return self._get_response(str(err), status_code=400)
        response, status_code = self.role_controller.create_role(role_data)
        print('response from RoleView.post()')
        print(response)
        return self._get_response(response, status_code=status_code)


    @login_required
    def get(self, role_id):
        role_data, status_code = self.role_controller.get_role(role_id)
        return self._get_response(role_data, status_code=status_code)

    @login_required
    def delete(self, role_id):
        result, status_code = self.role_controller.delete_role(role_id)
        return self._get_response(result, status_code=status_code)

    @login_required
    def put(self, role_id):
        user_id = request.json.get('user_id')
        result, status_code = self.role_controller.toggle_role(role_id, user_id)
        return self._get_response(result, status_code=status_code)


