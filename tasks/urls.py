from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tasks import views as TaskViews


router = DefaultRouter()
router.register('tasks', TaskViews.TaskViewSet)

app_name = 'tasks'

urlpatterns = [
    path(
        '',
        include(router.urls)
    ),

    path(
        'done/change/<int:pk>/',
        TaskViews.TaskChangeDoneStateAPIView.as_view(),
        name="task-done-change"
    ),
]
