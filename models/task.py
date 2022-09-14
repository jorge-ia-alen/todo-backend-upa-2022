class TaskModel():
    id = int
    description = str

    def __init__(self,id,description):
        self.id = id
        self.description = description

    def json(self, depth=0):
        json = {
            'id': self.id,
            'description': self.description
        }

        return json

