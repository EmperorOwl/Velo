""" Choices for the `Sprint` model. """

from django.db import models


class SprintStatus(models.IntegerChoices):
    """ Represents the status of a sprint. """
    ACTIVE = 1
    NOT_STARTED = 2
    COMPLETED = 3
