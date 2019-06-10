from rest_framework import viewsets, permissions
from api.models import *
from api.serializers import *

class UserProjectViewSet(viewsets.ModelViewSet):
    """
    API UserProjects memberships views
    """
    queryset = UserProject.objects.all()
    serializer_class = UserProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

class AssigneeViewSet(viewsets.ModelViewSet):
    """
    API Assignee views
    """
    queryset = Assignee.objects.all()
    serializer_class= AssigneeSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ProjectViewSet(viewsets.ModelViewSet):
    """
    API Projects views using DRF Viewsets
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(creator=user)

class TaskViewSet(viewsets.ModelViewSet):
    """
    API Tasks views using DRF Viewsets
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

class CommentViewSet(viewsets.ModelViewSet):
    """
    API Comment views using DRF Viewsets
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated,)

class BoardViewSet(viewsets.ModelViewSet):
    """
    API Board views using DRF Viewsets
    """
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticated,)

class PreferencesViewSet(viewsets.ModelViewSet):
    """
    API Preferences views using DRF Viewsets
    """
    queryset = Preferences.objects.all()
    serializer_class = PreferencesSerializer
    permission_classes = (permissions.IsAuthenticated,)

class NotificationViewSet(viewsets.ModelViewSet):
    """
    API Preferences views using DRF Viewsets
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (permissions.IsAuthenticated,)