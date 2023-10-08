from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from main.service import TaskCommandService
from rest_framework import status
from main.models import User, Task
# Create your views here.


class TaskAPIViewSet(ViewSet):

    def mark_completed(self, request):
        # This iwll mark task as completed and assign a new task task to freed user.

        task_id = request.data.get('task_id')
        user_id = request.auth['user_id']

        completed, msg = TaskCommandService().mark_task_as_completed(task_id=task_id, user_id=user_id)
        if completed:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND, data={"error":msg})



class UserAPIViewSet(ViewSet):

    def change_status(self, request):
        # This will mark a user as logged_in as per incoming request.

        user_id = request.auth['user_id']
        updated, _ = User.objects.filter(id=user_id).update(is_logged_in=True)

        if updated:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


