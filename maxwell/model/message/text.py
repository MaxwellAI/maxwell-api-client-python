from maxwell.model.base import Model


class TextMessage(Model):
    def __init__(self, text):
        self.text = text
        self.type = 'text'
