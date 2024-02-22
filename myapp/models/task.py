from django.db import models
from django.core import validators
from django.utils import timezone

from ..choices import TaskType, TaskPriority, TaskStatus
from ..utils import pretty_date, pretty_hour


def get_default_task_end_date():
    return timezone.now() + timezone.timedelta(days=3)


class Task(models.Model):
    """ Represents a task.
    Each task is linked to a sprint.
    Each task is related to a user through the concept of an assignee.
    """
    sprint = models.ForeignKey(
        'Sprint',
        on_delete=models.DO_NOTHING,
        related_name='tasks',
    )
    name = models.CharField(
        max_length=255
    )
    type = models.CharField(
        max_length=255,
        choices=TaskType.choices,
        default=TaskType.USER_STORY
    )
    start_date = models.DateTimeField(
        default=timezone.now
    )
    due_date = models.DateTimeField(
        default=get_default_task_end_date
    )
    story_points = models.IntegerField(
        default=5,
        validators=[
            validators.MinValueValidator(0),
            validators.MaxValueValidator(10)
        ]
    )
    priority = models.IntegerField(
        choices=TaskPriority.choices,
        default=TaskPriority.MEDIUM
    )
    status = models.IntegerField(
        choices=TaskStatus.choices,
        default=TaskStatus.NOT_STARTED
    )
    is_important = models.BooleanField(
        default=False
    )
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='tagged_tasks'
    )
    assignees = models.ManyToManyField(
        'User',
        through='Assignee',
        blank=True,
        related_name='assigned_tasks'
    )
    description = models.TextField(
        blank=True
    )

    def is_assigned_to(self, user) -> bool:
        """ Returns True if this task is assigned to a specific user. """
        return self.assignees.contains(user)

    def is_complete(self) -> bool:
        """ Returns True if this task is complete. """
        return self.status == TaskStatus.COMPLETED

    def log_time(self) -> float:
        """ Returns the total time worked on this task. """
        return sum(assignee.hours_worked for assignee in self.assignee_set.all())

    def get_start_date_display(self) -> str:
        """ Returns the string representation. """
        return pretty_date(self.start_date)

    def get_due_date_display(self) -> str:
        """ Returns the string representation. """
        return pretty_date(self.due_date)

    def get_story_points_display(self) -> str:
        """ Returns the string representation. """
        return str(self.story_points) + ' story points'

    def get_log_time_display(self) -> str:
        """ Returns the string representation. """
        return pretty_hour(self.log_time())

    def __str__(self) -> str:
        """ Returns the string representation. """
        return self.name
