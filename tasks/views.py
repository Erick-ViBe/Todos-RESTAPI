from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from tasks.models import Task
from tasks.serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """Task ViewSet: Create, Read, Update, Delete"""
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Retrieve the tasks for the authenticated user"""

        finished_task = self.request.query_params.get('done', None)
        queryset = self.queryset

        if finished_task is not None:
            finished_task = bool(int(finished_task))
            queryset = queryset.filter(done=finished_task)

        return queryset.filter(
            author=self.request.user
        ).order_by('-created_at')

    def perform_create(self, serializer):
        """Create a new Task"""
        serializer.save(author=self.request.user)


class TaskChangeDoneStateAPIView(APIView):
    """View that receive tasks id and change done state"""
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)

        if request.user == task.author:
            task.done = not task.done

            task.save()

            context = {
                'message': 'Successfully done state change'
            }

            return Response(data=context, status=status.HTTP_200_OK)

        else:

            context = {
                'message': 'You do not have permission to perform that action'
            }

            return Response(data=context, status=status.HTTP_401_UNAUTHORIZED)
