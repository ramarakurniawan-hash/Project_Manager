import uuid

class Project:
    def __init__(self, name, owner_id):
        self.id = str(uuid.uuid4())
        self.name = name
        self.owner_id = owner_id
        self.rows =[]