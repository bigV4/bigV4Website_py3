# coding: utf-8
from flask_restful import Api, Resource
api = Api()
@api.resource('/tmp_api')
class TmpApiResource(Resource):
    def get(self):
        pass