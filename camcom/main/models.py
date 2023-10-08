from django.db import models
from django.db.models import CheckConstraint, Q, UniqueConstraint

# Create your models here.


class User(models.Model):

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    is_free = models.BooleanField(default=True)
    is_logged_in = models.BooleanField(default=False)


class Task(models.Model):

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

