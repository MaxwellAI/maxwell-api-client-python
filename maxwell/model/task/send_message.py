from maxwell.model.base import Model


class SendMessageTask(Model):
    _include_fields = ('id',)

    def __init__(self, id, message):
        self.id = id
        self.message = message
        self.type = 'send_message'
