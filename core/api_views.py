from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Project, Task
from .serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        projects = Project.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct()

        return Task.objects.filter(project__in=projects)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)