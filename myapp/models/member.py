from django.db import models

from ..choices import MemberRole


class Member(models.Model):
    """ Represents the relationship between a Project and a User. """
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='members'
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )
    role = models.IntegerField(
        choices=MemberRole.choices,
        default=MemberRole.MEMBER
    )

    class Meta:
        # Ensures that the members are unique for a project.
        unique_together = ('project', 'user')
