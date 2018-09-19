from flask import request, Flask, redirect, url_for, render_template, flash
from flask_restplus import Resource
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from app.main.service.auth_helper import Auth
from ..util.dto import AuthDto
from app.main.util.oauth import OAuthSignIn
api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        return Auth.logout_user(data=auth_header)

@api.route('/authorize/<provider>')
@api.param('provider', 'The provider identifier')
class oauth_authorize(Resource):
    @api.doc('logout a user')
    def get(self,provider):
        if not current_user.is_anonymous:
            return "ass"
        oauth = OAuthSignIn.get_provider(provider)
        return oauth.authorize()

@api.route('/callback/<provider>')
@api.param('provider', 'The provider identifier')
class oauth_callback(Resource):
    @api.doc('logout a user')
    def get(self,provider):
        if not current_user.is_anonymous:
            return "ass"
        oauth = OAuthSignIn.get_provider(provider)
        social_id, username, email = oauth.callback()
        if social_id is None:
            print('Authentication failed.')
            return None
        # user = User.query.filter_by(social_id=social_id).first()
        # if not user:
        #     user = User(social_id=social_id, nickname=username, email=email)
        #     db.session.add(user)
        #     db.session.commit()
        login_user(user, True)
        print(social_id, username, email)
        return email