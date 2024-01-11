from django.db import models


class Tag(models.Model):
    """ Represents a tag. """
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        """ Returns the string representation. """
        return self.name
