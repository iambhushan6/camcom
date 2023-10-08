from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint

# Create your models here.


class User(models.Model):
    '''
    This model resembles fields related to a user of qc process
    Attributes:
    1. name
    2. email
    3. is_free (bool): If the user is associated with any task or not.
    4. is_logged_in (bool): If the user is logged in to its system or not.
    '''

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    is_free = models.BooleanField(default=True)
    is_logged_in = models.BooleanField(default=False)


class Task(models.Model):
    '''
    This model resembles fields related to a Task of qc process.
    
    Attributes:
    1. assigned_to (User) : This stores value of user id who has to perform this task, it can be null only untill task status is unassigned.
    2. name (str) : Name of task
    3. description (str) : Description of task
    4. status (str): status can have one of three value as: unassigned/assigned/completed. This will tell current state of task and will be changed according to assignment logic.

    Constraint: The CheckConstraint states that assigned_to fields value cannot be null when the status of task is either of assigned or completed.
    '''

    class TaskStatus(models.TextChoices):
        UNASSIGNED = 'unassigned'
        ASSIGNED = 'assigned'
        COMPLETED = 'completed'

    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    name = models.CharField(max_length=800, unique=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.UNASSIGNED)


    class Meta:
        constraints = [
            CheckConstraint(
                check= ~Q( Q(assigned_to__isnull=True)
                & Q(status__in=['assigned','completed'])),
                name="assigned_to_cannot_be_null_when_task_is_assigned_or_completed",
            )
        ]

