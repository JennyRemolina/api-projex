from rest_framework import serializers
from users.models import CustomUser
from api.models import *
from users.serializers import UserSerializer
import pdb

######################### FILTERS #############################################

class UserFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Queryset filter for current user
    """
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(UserFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(user=request.user)


class UserFilteredByProjectPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Queryset filter for current project
    """
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(UserFilteredByProjectPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None
        return queryset.filter(project=request.data.project)

####################### MODELS SERIALIZERS ##########################################


class UserProjectSerializer(serializers.ModelSerializer):
    """
    Intermediate model between user and project (known as membership)
    """
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(), required=False)

    class Meta:
        model = UserProject
        fields = ('id', 'user', 'project', 'role', 'status')

class AssigneeSerializer(serializers.ModelSerializer):
    """
    Assignee serializer (relationship between user and task)
    """
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), required=False)

    class Meta:
        model = Assignee
        fields = ('id', 'user', 'task')


class BoardSerializer(serializers.ModelSerializer):
    """
    Tasks container serializer
    """
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())

    class Meta:
        model = Board
        fields = ('id', 'title', 'project')

class TaskSerializer(serializers.ModelSerializer):
    """
    Each task created for a project
    """
    board = serializers.PrimaryKeyRelatedField(
        queryset=Board.objects.all())
    task_to_user = AssigneeSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'priority', 'task_file',
        'board', 'task_to_user')

    def create(self, validated_data):
        try:
            users_data = validated_data.pop('task_to_user')
        except KeyError as k:
            users_data = {}
        task = Project.objects.create(**validated_data)
        for data in users_data:
            UserProject.objects.create(task=task, **data)
        return task

class CommentSerializer(serializers.ModelSerializer):
    """
    Comments shown in task edit menu
    """
    creator = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())
    task = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all())

    class Meta:
        model=Comment
        fields = ('id', 'text', 'task', 'creator')

class ProjectSerializer(serializers.ModelSerializer):
    """
    Every project created by users. It uses a nested serializer to show
    memberships
    """
    creator = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())
    project_to_user = UserProjectSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = ('id', 'title', 'description',
                  'project_photo', 'creator', 'project_to_user')

    def create(self, validated_data):
        try:
            users_data = validated_data.pop('project_to_user')
        except KeyError as k:
            users_data = {}

        project = Project.objects.create(**validated_data)
        for data in users_data:
            UserProject.objects.create(project=project, **data)
        return project

class PreferencesSerializer(serializers.ModelSerializer):
    """
    User preferences serializer
    """
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all())

    class Meta:
        model = Preferences
        fields = ('id', 'language', 'color_schema', 'user')

    ######## TODO UPDATE USING PROJECT VIEW ##############


    # def update(self, instance, validated_data):
    #     users_data = validated_data.pop('project_to_user')
    #     assignee_data = UserProject.objects.get(project=instance)
    #     instance.update(**validated_data)
    #     for data in assignee_data:
    #         data.create_or_update(**users_data)
            
class NotificationSerializer(serializers.ModelSerializer):
    """
    Notifications serializer
    """

    class Meta:
        model = Notification
        fields = ('id', 'notifier_type', 'notifier')