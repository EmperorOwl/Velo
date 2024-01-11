""" Choices for the `User` model. """

from django.db import models


class UserRole(models.IntegerChoices):
    """ Represents the role of a user. """
    GUEST = 0
    MEMBER = 1
    SCRUM_MASTER = 2
    PRODUCT_OWNER = 3
