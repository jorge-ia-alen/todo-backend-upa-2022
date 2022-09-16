from models.task import TaskModel
from flask_restful import Resource,reqparse
from flasgger import swag_from
from flask import request

from utils import paginated_results,restrict


class Task(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id',type=int)
    parser.add_argument('descrip', type = str)
    parser.add_argument('status', type=str)

    @swag_from('../swagger/task/get_task.yaml')
    def get(self, id):
        tarea = TaskModel.find_by_id(id)
        if tarea:
            return tarea.json()
        return {'message':'No se encuentra la Tarea'},404
    
    @swag_from('../swagger/task/put_task.yaml')
    def put(self, id):
        tarea = TaskModel.find_by_id(id)
        if tarea:
            newdata = Task.parser.parse_args()
            tarea.from_reqparse(newdata)
            tarea.save_to_db()
            return tarea.json()

    @swag_from('../swagger/task/delete_task.yaml')
    def delete(self, id):
        tarea = TaskModel.find_by_id(id)
        if tarea:
            tarea.delete_from_db()
        
        return {'message': 'Se ha borrado la tarea'}

class TaskList(Resource):
    @swag_from('../swagger/task/list_task.yaml')
    def get(self):
        query = TaskModel.query
        return paginated_results(query)
    
    @swag_from('../swagger/task/post_task.yaml')
    def post(self):
        data = Task.parser.parse_args()

        tarea = TaskModel(**data)

        try:
            tarea.save_to_db()
        except Exception as e:
            print(e)
            return {'message':'Ocurrio un error al crear la tarea'}, 500

        return tarea.json(), 201

class TaskSearch(Resource):
    @swag_from('../swagger/task/search_task.yaml')
    def post(self):
        query = TaskModel.query
        if request.json:
            filtros = request.json
            query = restrict(query,filtros,'id',lambda x: TaskModel.id  == x)
            query = restrict(query,filtros,'descrip',lambda x: TaskModel.descrip.contains(x))
            query = restrict(query,filtros,'status',lambda x: TaskModel.status.contains(x))

        return paginated_results(query)