from maxwell.model.base import Model


class SendMessageTask(Model):
    _include_fields = ("id",)

    def __init__(self, id, message, next_task_id=None):
        self.id = id
        self.message = message
        self.type = "send_message"
        self.next_task = {"id": next_task_id} if next_task_id else None
