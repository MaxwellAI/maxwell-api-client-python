from maxwell.model.base import Model


class Workflow(Model):
    def __init__(self, tasks):
        self.tasks = tasks
        self.start_task = {'id': tasks[0].id}
