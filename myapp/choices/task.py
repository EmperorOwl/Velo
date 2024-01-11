""" Choices for the `Task` model. """

from django.db import models


class TaskType(models.TextChoices):
    """ Represents the type of a task. """
    BUG = 'B'
    USER_STORY = 'U'


class TaskPriority(models.IntegerChoices):
    """ Represents the priority of a task. """
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class TaskStatus(models.IntegerChoices):
    """ Represents the status of a task. """
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3
