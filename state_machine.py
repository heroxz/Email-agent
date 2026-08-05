from enum import Enum, auto

class TaskState(Enum):
    INIT = auto()
    PARSED = auto()
    CLASSIFIED = auto()
    SUMMARIZED = auto()
    REPLIED = auto()
    ARCHIVED = auto()
    COMPLETED = auto()

class StateMachine:
    def __init__(self):
        self.state = TaskState.INIT

    def next(self):
        if self.state == TaskState.INIT:
            self.state = TaskState.PARSED
        elif self.state == TaskState.PARSED:
            self.state = TaskState.CLASSIFIED
        elif self.state == TaskState.CLASSIFIED:
            self.state = TaskState.SUMMARIZED
        elif self.state == TaskState.SUMMARIZED:
            self.state = TaskState.REPLIED
        elif self.state == TaskState.REPLIED:
            self.state = TaskState.ARCHIVED
        elif self.state == TaskState.ARCHIVED:
            self.state = TaskState.COMPLETED
        return self.state

    def is_terminal(self):
        return self.state == TaskState.COMPLETED

    def reset(self):
        self.state = TaskState.INIT

        
        
