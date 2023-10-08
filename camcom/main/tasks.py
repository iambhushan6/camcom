from main.models import User, Task
from main.service import TaskCommandService
from celery import shared_task


@shared_task(bind=True)
def scheduled_task_assign_tasks_to_free_users(self):
    '''
    This task can be scheduled at every minute. In this task all logged in and free users will be fetched from db and given to TaskCommandService to assign them pending tasks.
    '''

    logged_in_free_users = list(User.objects.filter(logged_in=True, is_free=True))
    TaskCommandService().assign_unassigned_tasks(users=logged_in_free_users)

    return