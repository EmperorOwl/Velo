from django.db import models
from django.contrib.auth.models import AbstractUser

from ..choices import TaskStatus
from ..utils import Progress, pretty_hour, pretty_date


class User(AbstractUser):
    """ Represents a user.
    Each user is linked to the project they last viewed.
    """
    last_visited_project = models.ForeignKey(
        'Project',
        on_delete=models.SET_NULL,
        null=True
    )
    is_guest = models.BooleanField(
        default=False
    )

    def set_last_visited_project(self, project):
        """ Setter """
        self.last_visited_project = project
        self.save()

    def tasks(self, project=None, sprint=None):
        """ Returns the tasks assigned to this user.
        Can filter by project and/or sprint.
        Orders tasks by due date from oldest to newest.
        """
        tasks = self.assigned_tasks.all()
        tasks = tasks.filter(sprint__project=project) if project else tasks
        tasks = tasks.filter(sprint=sprint) if sprint else tasks
        tasks.order_by('due_date')
        return tasks

    def completed_tasks(self, project=None, sprint=None):
        """ Returns the tasks assigned to this user that are complete.
        Can filter by project and/or sprint.
        Orders tasks by due date from oldest to newest.
        """
        return self.tasks(project, sprint).filter(status=TaskStatus.COMPLETED)

    def remaining_tasks(self, project=None, sprint=None) -> list:
        """ Returns the tasks assigned to this user that are incomplete.
        Can filter by project and/or sprint.
        Orders tasks by due date from oldest to newest.
        """
        return self.tasks(project, sprint).exclude(status=TaskStatus.COMPLETED)

    def task_progress(self, project=None, sprint=None) -> Progress:
        """ Returns the progress on the assigned tasks of this user.
        Can filter by project and/or sprint.
        """
        return Progress(
            total=len(self.tasks(project, sprint)),
            completed=len(self.completed_tasks(project, sprint))
        )

    def log_time(self, project=None, sprint=None) -> int:
        """ Returns the total time worked by this user.
        Can filter by project and/or sprint.
        """
        res = 0
        for task in self.tasks(project, sprint):
            res += task.assignee_set.filter(user=self).first().hours_worked
        return res

    def get_log_time_display(self, project=None, sprint=None) -> str:
        """ Returns the string representation. """
        return pretty_hour(self.log_time(project, sprint))

    def get_last_login_display(self) -> str:
        """ Returns the string representation. """
        return pretty_date(self.last_login)

    def __str__(self):
        """ Returns the string representation. """
        return self.get_full_name()
