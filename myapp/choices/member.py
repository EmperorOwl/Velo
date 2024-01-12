""" Choices for the `Member` model. """

from django.db import models


class MemberRole(models.IntegerChoices):
    """ Represents the role of a user in a project. """
    GUEST = 0
    MEMBER = 1
    SCRUM_MASTER = 2
    PRODUCT_OWNER = 3
