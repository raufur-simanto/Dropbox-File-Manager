import requests
from flask import current_app as app
from flask import make_response, request
from flask_restx import Namespace, Resource, fields

file_namespace = Namespace("files", description="File operations")

APP_KEY = app.config.get("APP_KEY")
APP_SECRET = app.config.get("APP_SECRET")
REDIRECT_URI = app.config.get("REDIRECT_URI")

file_model = file_namespace.model(
    "File",
    {
        "name": fields.String(required=True, description="The name of the file"),
        "path_lower": fields.String(
            required=True, description="The lowercase path of the file"
        ),
        "id": fields.String(required=True, description="The file ID"),
        "size": fields.Integer(
            required=True, description="The size of the file in bytes"
        ),
    },
)
file_list_model = file_namespace.model(
    "file_list_model", {"files": fields.Nested(file_model)}
)

search_file_model = file_namespace.model(
    "SearchFile",
    {
        "file_name": fields.String(
            required=True, description="The name of the file to search for"
        ),
        "path": fields.String(
            required=False, description="The path of the file to search for"
        ),
    },
)

rename_file_model = file_namespace.model(
    "RenameFile",
    {
        "current_name": fields.String(
            required=True, description="The previous name of the file"
        ),
        "new_name": fields.String(
            required=True, description="The new name of the file"
        ),
        "path": fields.String(required=False, description="path for the file"),
    },
)


class DownloadFile(Resource):
    def get(self, path):
        """Download a file"""
        access_token = request.headers.get("Authorization")

        if not access_token:
            file_namespace.abort(401, "Access token is missing")

        headers = {
            "Authorization": access_token,
            "Dropbox-API-Arg": f'{{"path": "/{path}"}}',
        }

        response = requests.post(
            "https://content.dropboxapi.com/2/files/download", headers=headers
        )
        app.logger.info(f"Status code: {response.status_code}")
        app.logger.info(f"Headers: {response.headers}")
        app.logger.info(f"Response content length: {len(response.content)}")

        if response.status_code != 200:
            app.logger.error(f"Failed to download file: {response.text}")
            file_namespace.abort(response.status_code, "Failed to download file")

        file_response = make_response(response.content)

        # Set headers to indicate file download
        file_name = path.split("/")[-1]  # Extract file name from path
        file_response.headers["Content-Type"] = "application/octet-stream"
        file_response.headers["Content-Disposition"] = (
            f"attachment; filename={file_name}"
        )

        app.logger.info(f"file name: {file_name}, file response {file_response}")

        return file_response


class GetAllFiles(Resource):
    def get(self):
        """Get all files"""
        access_token = request.headers.get("Authorization")

        if not access_token:
            file_namespace.abort(401, "Access token is missing")
        headers = {"Authorization": access_token, "Content-Type": "application/json"}
        data = {"path": "", "recursive": True}
        response = requests.post(
            "https://api.dropboxapi.com/2/files/list_folder", headers=headers, json=data
        )
        print(response.json())
        if response.status_code != 200:
            file_namespace.abort(response.status_code, "Failed to list files")
        response_data = {"data": response.json(), "status": "success"}
        return response_data, 200


class SearchFiles(Resource):
    @file_namespace.expect(search_file_model)
    def post(self):
        """Search a specific file"""
        payload = request.get_json()
        access_token = request.headers.get("Authorization")

        if not access_token:
            file_namespace.abort(401, "Access token is missing")

        headers = {"Authorization": access_token, "Content-Type": "application/json"}
        data = {
            "path": payload.get("path", ""),
            "query": f"/{payload.get('file_name')}",
        }
        response = requests.post(
            "https://api.dropboxapi.com/2/files/search_v2", headers=headers, json=data
        )

        if response.status_code != 200:
            file_namespace.abort(response.status_code, "Failed to search files")
        # app.logger.info(f"available files: {response.json()}")

        matches = response.json().get("matches", [])
        app.logger.info(f"matches: {matches}")
        if matches:
            data = []
            for match in matches:
                if match["metadata"]["metadata"]["name"] == payload.get("file_name"):
                    data.append(match)

            response_data = {"data": data, "status": "success"}
            return response_data, 200
        return {"data": "This file is not found!", "status": "failed"}, 200


class UploadFile(Resource):
    def post(self):
        """Upload a file"""
        access_token = request.headers.get("Authorization")

        if not access_token:
            file_namespace.abort(401, "Access token is missing")

        if "file" not in request.files:
            file_namespace.abort(400, "No file part in the request")
        app.logger.info(f"request: {request}")
        data = request.form.to_dict()

        file = request.files["file"]
        path = data.get("path", "")
        if path:
            arg_value = f'{{"path": "{path}/{file.filename}","mode": "add","autorename": true,"mute": false}}'

        else:
            arg_value = (
                '{"path": "/'
                + file.filename
                + '","mode": "add","autorename": true,"mute": false}'
            )

        if file.filename == "":
            file_namespace.abort(400, "No selected file")

        headers = {
            "Authorization": access_token,
            "Dropbox-API-Arg": arg_value,
            "Content-Type": "application/octet-stream",
        }
        response = requests.post(
            "https://content.dropboxapi.com/2/files/upload", headers=headers, data=file
        )
        print(response.status_code)
        print(response.json())

        if response.status_code != 200:
            file_namespace.abort(response.status_code, "Failed to upload file")
        response_data = {
            "data": response.json(),
            "status": "success",
            "message": "File uploaded successfully",
        }
        return response_data, 200


class DeleteFile(Resource):
    def delete(self, path):
        """Delete a file"""
        access_token = request.headers.get("Authorization")

        if not access_token:
            file_namespace.abort(401, "Access token is missing")

        headers = {"Authorization": access_token, "Content-Type": "application/json"}
        data = {"path": "/" + path}
        response = requests.post(
            "https://api.dropboxapi.com/2/files/delete_v2", headers=headers, json=data
        )

        if response.status_code != 200:
            app.logger.info(f"response: {response.json()}")
            file_namespace.abort(response.status_code, "Failed to delete file")

        return {"message": "File deleted successfully"}, 204


class CountFiles(Resource):
    def get(self):
        """Count the number of files"""
        access_token = request.headers.get("Authorization")

        if not access_token:
            file_namespace.abort(401, "Access token is missing")

        headers = {"Authorization": access_token, "Content-Type": "application/json"}
        data = {"path": "", "recursive": True}
        response = requests.post(
            "https://api.dropboxapi.com/2/files/list_folder", headers=headers, json=data
        )

        if response.status_code != 200:
            file_namespace.abort(response.status_code, "Failed to list files")

        entries = response.json().get("entries", [])
        file_count = sum(1 for entry in entries if entry[".tag"] == "file")

        return {"file_count": file_count}, 200


class RenameFile(Resource):
    @file_namespace.expect(rename_file_model)
    def put(self):
        """Rename a file"""
        access_token = request.headers.get("Authorization")
        data = request.get_json()
        print(data)

        if not access_token:
            file_namespace.abort(401, "Access token is missing")

        headers = {"Authorization": access_token, "Content-Type": "application/json"}
        path = data.get("path") if data.get("path") else ""
        payload = {
            "from_path": f"{path}/{data.get('current_name')}",
            "to_path": f"{path}/{data.get('new_name')}",
        }

        response = requests.post(
            "https://api.dropboxapi.com/2/files/move_v2", headers=headers, json=payload
        )
        app.logger.info(f"response:: {response.json()}")

        if response.status_code != 200:
            file_namespace.abort(response.status_code, "Failed to rename file")
        response_data = {
            "data": response.json(),
            "status": "success",
            "message": "File renamed successfully",
        }

        return response_data, 200


file_namespace.add_resource(DownloadFile, "/download/<path:path>")
file_namespace.add_resource(GetAllFiles, "/get_all_files")
file_namespace.add_resource(SearchFiles, "/search")
file_namespace.add_resource(UploadFile, "/upload")
file_namespace.add_resource(DeleteFile, "/delete/<path:path>")
file_namespace.add_resource(CountFiles, "/count")
file_namespace.add_resource(RenameFile, "/rename")
