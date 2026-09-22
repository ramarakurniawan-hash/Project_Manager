import uuid

class Task:
    def __init__(
        self,
        name,
        start_date,
        end_date,
        status,
        parent_id=None,
        order=0
    ):
        self.id = str(uuid.uuid4())
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.status = status
        self.parent_id = parent_id
        self.order = order

    @property
    def duration(self):
        return (self.end_date - self.start_date).days + 1