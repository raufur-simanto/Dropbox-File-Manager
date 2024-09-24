from flask import current_app as app
from flask import request, redirect
from flask_restx import Namespace, Resource, fields
import requests

from urllib.parse import urlencode

APP_KEY = app.config.get("APP_KEY")
APP_SECRET = app.config.get("APP_SECRET")
REDIRECT_URI = app.config.get("REDIRECT_URI")

auth_namespace = Namespace('auth', description='Authentication operations')


token_model = auth_namespace.model('Token', {
    'access_token': fields.String(required=True, description='The access token'),
    'token_type': fields.String(required=True, description='The token type'),
    'expires_in': fields.Integer(required=True, description='Token expiration time in seconds')
})


class Login(Resource):
    def get(self):
        """Initiate the OAuth2 login flow"""
        params = {
            "client_id": APP_KEY,
            "redirect_uri": REDIRECT_URI,
            "response_type": "code",
            "scope": "files.content.read files.content.write account_info.read files.metadata.read file_requests.read"
        }
        auth_url = f"https://www.dropbox.com/oauth2/authorize?{urlencode(params)}"
        print(f"Redirecting to {auth_url}")
        return redirect(auth_url)
    


class Callback(Resource):
    @auth_namespace.marshal_with(token_model)
    def get(self):
        code = request.args.get('code')
        if not code:
            return {"message": "Authorization code is missing"}, 400

        print(f"Received authorization code: {code}")

        token_url = "https://api.dropboxapi.com/oauth2/token"
        data = {
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "client_id": APP_KEY,
            "client_secret": APP_SECRET
        }
        response = requests.post(token_url, data=data)
        
        if response.status_code != 200:
            print(f"Failed to obtain access token. Status: {response.status_code}, Response: {response.text}")  # Debugging: Print the error
            return {"message": "Failed to obtain access token", "details": response.json()}, response.status_code

        return response.json(), 200
    
auth_namespace.add_resource(Login, "/login")
auth_namespace.add_resource(Callback, "/callback")