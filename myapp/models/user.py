from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

from ..choices import UserRole, TaskStatus
from ..utils import Progress


class User(AbstractUser):
    """ Represents a user. """
    role = models.IntegerField(
        choices=UserRole.choices,
        default=UserRole.MEMBER
    )
    last_visited_project = models.ForeignKey(
        'Project',
        on_delete=models.SET_NULL,
        null=True
    )

    def is_guest(self) -> bool:
        """ Returns True if this user is a guest. """
        return self.role == UserRole.GUEST

    def set_last_visited_project(self, project):
        """ Setter """
        self.last_visited_project = project
        self.save()

    def tasks(self, sprint=None):
        """ Returns this user's tasks.
        Can filter by sprint.
        Orders tasks by due date from oldest to newest.
        """
        tasks = self.assigned_tasks.all()
        tasks = tasks.filter(sprint=sprint) if sprint else tasks
        tasks.order_by('due_date')
        return tasks

    def completed_tasks(self, sprint=None):
        """ Returns this user's tasks that are complete.
        Can filter by sprint.
        Orders tasks by due date from oldest to newest.
        """
        return self.tasks(sprint).filter(status=TaskStatus.COMPLETED)

    def remaining_tasks(self, sprint=None) -> list:
        """ Returns this user's tasks that are incomplete.
        Can filter by sprint.
        Orders tasks by due date from oldest to newest.
        """
        return self.tasks(sprint).exclude(status=TaskStatus.COMPLETED)

    def task_progress(self, sprint=None) -> Progress:
        """ Returns this user's progress.
        Can filter by sprint.
        """
        return Progress(
            total=len(self.tasks(sprint)),
            completed=len(self.completed_tasks(sprint))
        )

    def log_time(self, sprint=None) -> int:
        """ Returns the total time worked by this user.
        Can filter by sprint.
        """
        return sum(task.log_time() for task in self.tasks(sprint))

    def get_log_time_display(self, sprint=None) -> str:
        """ Returns the string representation. """
        t = self.log_time(sprint)
        return str(t).replace('.0', '') + ' hour' + ('s' if t != 1 else '')

    def get_last_login_display(self) -> str:
        """ Returns the string representation. """
        d = self.last_login
        if not d:
            return ''
        return d.strftime('%b %d'
                          + (', %Y' if d.year != timezone.now().year else ''))

    def __str__(self):
        """ Returns the string representation. """
        return self.get_full_name()
