from django.db import models

from ..choices import MemberRole
from ..utils import pretty_hour


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

    def log_time(self):
        """ Returns the total time worked by this member on this project. """
        return self.user.log_time(self.project)

    def get_log_time_display(self) -> str:
        """ Returns the string representation. """
        return pretty_hour(self.log_time())

    class Meta:
        # Ensures that the members are unique for a project.
        unique_together = ('project', 'user')
