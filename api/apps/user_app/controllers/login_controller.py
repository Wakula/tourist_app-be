import uuid, time, json, redis, facebook
from marshmallow import ValidationError
from flask import current_app
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import AuthorizedSession
from google.auth.exceptions import GoogleAuthError


class LoginController:
    @classmethod
    def validate_fields(cls, email, password):
        user = current_app.models.User.get_user_by_email(email=email)

        if not user or not user.check_password(password):
            raise Exception('Incorrect email or password')

        if not user.is_active:
            return Exception('Your account is not active')

        return user

    @classmethod
    def login(cls, data):
        try:
            user = cls.validate_fields(**data)
        except Exception as e:
            return str(e), 400
        session_id = cls._create_session(user=user)

        data = {
            'session_id': session_id,
            'user_id': user.user_id
        }
        return data, 200
    
    @classmethod
    def login_with_social(cls, data):
        user_data = cls._authorize_user(token=data['auth_token'], provider=data['provider'])
        
        user = current_app.models.User.get_user_by_email(email=user_data['email'])

        if not user:
            user = current_app.models.User.create_user(**user_data, is_active=True)
        elif not user.is_active:
            user.activate_user()
        session_id = cls._create_session(user=user)
        data = {
            'session_id': session_id,
            'user_id': user.user_id
        }
        return data, 200
    
    @classmethod
    def _authorize_user(cls, token, provider):
        if provider == 'FACEBOOK':
            return cls._authorize_with_fb(token)
        if provider == 'GOOGLE':
            return cls._authorize_with_google(token)


    @staticmethod
    def _authorize_with_fb(token):
        try:
            graph = facebook.GraphAPI(access_token=token)
            raw_data = graph.get_object(id="me", fields='first_name, last_name, email, picture')
        except facebook.GraphAPIError as e:
            raise ValidationError(e.message)

        user_data = {
            'name': raw_data['first_name'],
            'surname': raw_data['last_name'],
            'email': raw_data['email'],
            'avatar': raw_data['picture']['data']['url']
        }
        return user_data

    @staticmethod
    def _authorize_with_google(token):
        credentials = Credentials(token)
        authed_session = AuthorizedSession(credentials)
        response = authed_session.get('https://www.googleapis.com/oauth2/v1/userinfo?alt=json')

        raw_data = json.loads(response.text)
        user_data = {
            'name': raw_data['given_name'],
            'surname': raw_data['family_name'],
            'email': raw_data['email'],
            'avatar': raw_data['picture']
        }
        return user_data

    @classmethod
    def _create_session(cls, user):
        session_id = str(uuid.uuid1())
        login_time = 24 * 60 * 60
        started_at = time.time()
        expired_at = started_at + login_time
        session_data = {
            'user_id': user.user_id,
            'started_at': started_at,
            'expired_at': expired_at,
        }
        with redis.Redis() as redis_client:
            redis_client.set(session_id, json.dumps(session_data), ex=login_time)

        return session_id
