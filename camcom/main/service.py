from main.models import User, Task
from django.db import transaction
from typing import List

class TaskCommandService:

    def __init__(self) -> None:
        pass
    
    def mark_task_as_completed(self, task_id:int, user_id:int):
        # This function marks incoming task as completed and incoming user as free once task is completed. A free user is then assigned task accordingly.

        try:
            with transaction.atomic():
                Task.objects.filter(id=task_id).update(status=Task.TaskStatus.COMPLETED)
                User.objects.filter(id=user_id).update(is_free=True)
        except Exception as e:
            return False, str(e)
        
        user = User.objects.filter(id=user_id).first()
        if user.is_logged_in and user.is_free:
            self.assign_unassigned_tasks(users=[user])
        return True, "successful."


    def assign_unassigned_tasks(self, users: List[User]):
        # This function assigns unassigned tasks to incoming users and notifies them about it.

        tasks = Task.objects.filter(status=Task.TaskStatus.UNASSIGNED)[:len(users)]
        user_task_map = {}

        try:
            with transaction.atomic():

                for index, task in enumerate(tasks):
                    user = users[index]
                    assert user.is_free == True
                    assert user.is_logged_in == True
                    task.assigned_to = user
                    task.status = Task.TaskStatus.ASSIGNED
                    task.save(update_fields=['assigned_to','status'])

                    user.is_free = False
                    user.save(update_fields=['is_free'])
                    user_task_map[user] = task
        except Exception as e:
            return False, str(e)

        # Call Messeing service to send notification/mail to assigned users about task
        for user, task in user_task_map.items():
            # send_email_to_users_for_respective_task(task=task, user=user)
            pass

        return True, "task assigned successfully."