class ToolContext:

    def __init__(self, session):
        self.session = session
        self.data = session.last_tool_result or {}

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value

    def remove(self, key):
        self.data.pop(key, None)

    def save(self):
        self.session.last_tool_result = self.data
        self.session.save(update_fields=["last_tool_result"])