from django.contrib import admin
from django.urls import path
from main.views import UserAPIViewSet, TaskAPIViewSet

urlpatterns = [
    path('task/mark-completed/', TaskAPIViewSet.as_view({"post":"mark_completed"}), name="task_status_change_view"),
    path('user/logged-in/', UserAPIViewSet.as_view({"get":"change_status"}), name="mark_user_logged_in_view")
]
