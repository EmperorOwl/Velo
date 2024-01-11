from django.db import models


class Assignee(models.Model):
    """ Represents the relationship between a Task and a User. """
    task = models.ForeignKey(
        'Task',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )
    hours_worked = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0
    )

    class Meta:
        # Ensures that the assignees are unique for a task.
        unique_together = ('task', 'user')
