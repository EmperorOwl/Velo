""" Choices for the `Project` model. """

from django.db import models


class ProjectStatus(models.IntegerChoices):
    """ Represents the status of a project. """
    ACTIVE = 1
    NOT_STARTED = 2
    COMPLETED = 3
