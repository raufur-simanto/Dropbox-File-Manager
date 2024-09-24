import os

import jwt
from flask import abort, request

def token_required(f):
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return {'message': 'Token is missing!'}, 403
        return f(token, *args, **kwargs)
    return decorated