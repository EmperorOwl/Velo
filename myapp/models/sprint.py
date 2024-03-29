from django.db import models
from django.utils import timezone

from ..choices import SprintStatus, TaskStatus
from ..utils import Progress, pretty_date, pretty_hour


def get_default_sprint_end_date():
    return timezone.now() + timezone.timedelta(weeks=2)


class Sprint(models.Model):
    """ Represents a sprint.
    Each sprint is linked to a project.
    """
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='sprints',
    )
    name = models.CharField(
        max_length=255
    )
    start_date = models.DateTimeField(
        default=timezone.now
    )
    end_date = models.DateTimeField(
        default=get_default_sprint_end_date
    )
    status = models.IntegerField(
        choices=SprintStatus.choices,
        default=SprintStatus.NOT_STARTED
    )
    goal = models.TextField(
        blank=True
    )

    def completed_tasks(self) -> list:
        """ Returns the tasks in this sprint that are complete. """
        return self.tasks.filter(status=TaskStatus.COMPLETED)

    def point_progress(self):
        """ Returns the progress on the story points of this sprint. """
        return Progress(
            total=sum(task.story_points for task in self.tasks.all()),
            completed=sum(task.story_points for task in self.completed_tasks())
        )

    def task_progress(self):
        """ Returns the progress on the tasks of this sprint. """
        return Progress(
            total=len(self.tasks.all()),
            completed=len(self.completed_tasks())
        )

    def log_time(self) -> int:
        """ Returns the total number of hours worked on this sprint. """
        return sum(task.log_time() for task in self.tasks.all())

    def get_start_date_display(self) -> str:
        """ Returns the string representation. """
        return pretty_date(self.start_date)

    def get_end_date_display(self) -> str:
        """ Returns the string representation. """
        return pretty_date(self.end_date)

    def get_log_time_display(self) -> str:
        """ Returns the string representation. """
        return pretty_hour(self.log_time())

    def __str__(self) -> str:
        """ Returns the string representation. """
        return self.name
