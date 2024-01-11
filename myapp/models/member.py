from django.db import models


class Member(models.Model):
    """ Represents the relationship between a Project and a User. """
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )

    class Meta:
        # Ensures that the members are unique for a project.
        unique_together = ('project', 'user')
