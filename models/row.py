class Row:
    def __init__(self, content=None):
        self.content = content

    @property
    def is_blank(self):
        return self.content is None