import requests
from flask import current_app as app
from flask import request
from flask_restx import Namespace, Resource, fields

profile_namespace = Namespace("profile", description="User profile operations")

profile_model = profile_namespace.model(
    "Profile",
    {
        "account_id": fields.String(required=True, description="The account ID"),
        "name": fields.String(required=True, description="The user's name"),
        "email": fields.String(required=True, description="The user's email"),
        "country": fields.String(required=True, description="The user's country"),
    },
)

APP_KEY = app.config.get("APP_KEY")
APP_SECRET = app.config.get("APP_SECRET")
REDIRECT_URI = app.config.get("REDIRECT_URI")


class ProfileInfo(Resource):
    @profile_namespace.marshal_with(profile_model)
    def get(self):
        """Get user profile information"""
        access_token = request.headers.get("Authorization")
        print(access_token)

        if not access_token:
            profile_namespace.abort(401, "Access token is missing")

        headers = {"Authorization": access_token}
        response = requests.post(
            "https://api.dropboxapi.com/2/users/get_current_account", headers=headers
        )
        print(response.json())
        if response.status_code != 200:
            profile_namespace.abort(
                response.status_code, "Failed to get profile information"
            )

        data = response.json()
        resp_data = {
            "account_id": data["account_id"],
            "name": data["name"]["display_name"],
            "email": data["email"],
            "country": data["country"],
        }
        return resp_data, 200


profile_namespace.add_resource(ProfileInfo, "/user-info")
