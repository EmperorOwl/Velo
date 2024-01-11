from django.db import models
from django.utils import timezone

from ..choices import ProjectStatus
from ..utils import Progress


class Project(models.Model):
    """ Represents a project. """
    name = models.CharField(
        max_length=255
    )
    start_date = models.DateTimeField(
        default=timezone.now
    )
    end_date = models.DateTimeField(
        default=timezone.now() + timezone.timedelta(weeks=6)
    )
    status = models.IntegerField(
        choices=ProjectStatus.choices,
        default=ProjectStatus.NOT_STARTED
    )
    description = models.TextField(
        blank=True
    )
    team = models.ManyToManyField(
        'User',
        through='Member',
        blank=True,
        related_name='projects'
    )

    def is_complete(self) -> bool:
        """ Returns True if this project is complete. """
        return self.status == ProjectStatus.COMPLETED

    def point_progress(self) -> Progress:
        """ Returns the progress on the story points of this project. """
        sprints = [sprint.point_progress() for sprint in self.sprints.all()]
        return Progress(
            total=sum(progress.total for progress in sprints),
            completed=sum(progress.completed for progress in sprints)
        )

    def task_progress(self) -> Progress:
        """ Returns the progress on the tasks of this project. """
        sprints = [sprint.task_progress() for sprint in self.sprints.all()]
        return Progress(
            total=sum(progress.total for progress in sprints),
            completed=sum(progress.completed for progress in sprints)
        )

    def log_time(self) -> int:
        """ Returns the total time worked on this project. """
        return sum(sprint.log_time() for sprint in self.sprints.all())

    def get_log_time_display(self) -> str:
        """ Returns the string representation. """
        t = self.log_time()
        return str(t).replace('.0', '') + ' hour' + ('s' if t != 1 else '')

    def __str__(self) -> str:
        """ Returns the string representation. """
        return self.name
