import requests
from flask import current_app as app
from flask import make_response, request
from flask_restx import Namespace, Resource, fields

folder_namespace = Namespace("files", description="File operations")

APP_KEY = app.config.get("APP_KEY")
APP_SECRET = app.config.get("APP_SECRET")
REDIRECT_URI = app.config.get("REDIRECT_URI")

create_folder_model = folder_namespace.model(
    "create_folder_model",
    {"path": fields.String(required=True, description="path for the folder")},
)


class CreateFolder(Resource):
    @folder_namespace.expect(create_folder_model)
    def post(self):
        """Create a folder"""
        access_token = request.headers.get("Authorization")
        if not access_token:
            folder_namespace.abort(401, "Authentication failed!")
        payload = request.get_json()
        app.logger.info(f"payload: {payload}")

        data = {"autorename": False, "path": payload.get("path", "/")}
        headers = {"Authorization": access_token, "Content-Type": "application/json"}

        response = requests.post(
            "https://api.dropboxapi.com/2/files/create_folder_v2",
            headers=headers,
            json=data,
        )

        if response.status_code != 200:
            app.logger.info(
                f"response status: {response.status_code}, response: {response.json()}"
            )
            folder_namespace.abort(response.status_code, "Failed to create a folder")

        app.logger.info(
            f"response status: {response.status_code}, response: {response.json()}"
        )
        response_data = {"data": response.json(), "status": "success"}
        return response_data, 201


folder_namespace.add_resource(CreateFolder, "/create")
