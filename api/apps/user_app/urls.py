from . import views


urls = {
    '/v1/user': views.UserView.as_view('user'),
    '/v1/user/avatar': views.UserAvatarView.as_view('user_avatar'),
    '/v1/login': views.LoginView.as_view('login'),
    '/v1/logout': views.LogoutView.as_view('logout'),
}