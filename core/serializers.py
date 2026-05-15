from rest_framework import serializers
from .models import Project, Task


class ProjectSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'owner_name', 'members', 'status', 'created_at']
        read_only_fields = ['owner', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'project',
            'project_name',
            'assigned_to',
            'assigned_to_name',
            'created_by',
            'status',
            'priority',
            'due_date',
            'created_at',
            'is_overdue',
        ]
        read_only_fields = ['created_by', 'created_at', 'is_overdue']