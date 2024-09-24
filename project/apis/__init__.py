from flask_restx import Api

api = Api(
    title="Dropbox File Manager API",
    version="1.0",
    description="A simple File Manager API",
)


from project.apis.auth import auth_namespace
from project.apis.files import file_namespace
from project.apis.folders import folder_namespace
from project.apis.profile import profile_namespace

api.add_namespace(auth_namespace, path="/auth")
api.add_namespace(file_namespace, path="/file")
api.add_namespace(profile_namespace, path="/profile")
api.add_namespace(folder_namespace, path="/folder")
