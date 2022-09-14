import os
from flask import Flask, redirect
from resources.task import Task
from flask_restful import Api
from flasgger import Swagger

app = Flask(__name__)


api = Api(app,errors = {
		''
	})

PREFIX = os.environ.get('PREFIX_PATH', '/api')

# Swagger config
app.config['SWAGGER'] = {
	'title': 'todo_backend',
	'version': '1.0.0',
	'description': 'API de servicios REST en Flask',
	'uiversion': 2,
	'tags': [{'name': 'jwt'}],
	'specs': [{
		'endpoint': 'apispec_1',
		'route': f'{PREFIX}/apispec_1.json',
		'rule_filter': lambda rule: True, # all in
		'model_filter': lambda tag: True # all in
	}],
	'specs_route': f"{PREFIX}/apidocs/",
	'static_url_path': f'{PREFIX}/static'
}
swagger = Swagger(app)

@app.route("/")
@app.route(f"{PREFIX}/")
def welcome():
    return redirect(f"{PREFIX}/apidocs",code=302)

api.add_resource(Task,f'{PREFIX}/task/<id>')

if __name__ == '__main__':
    app.run()
