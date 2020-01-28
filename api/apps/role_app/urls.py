from . import views

urls = {
    '/v1/role/<int:role_id>': views.RoleView.as_view('role'),
    '/v1/role': views.RoleView.as_view('add_role'),
}
