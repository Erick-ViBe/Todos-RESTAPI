from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task objects"""

    class Meta:
        model = Task
        fields = ('id', 'content', 'done', 'created_at')
        read_only_fields = ('id', 'created_at')
