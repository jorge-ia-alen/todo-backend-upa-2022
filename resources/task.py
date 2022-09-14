
from models.task import TaskModel
from flask_restful import Resource, reqparse
from flasgger import swag_from

class Task(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('id', type=int)
    parser.add_argument('description', type = str)

    @swag_from('../swagger/task/get_task.yaml')
    def get(self,id):
        tarea = TaskModel(Resource)
        if tarea:
            return tarea.json()
        return {'message':'No se encuentra la Tarea'},404