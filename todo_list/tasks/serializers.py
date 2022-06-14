from rest_framework import serializers

from .models import Task


# Task Serializer
class TaskSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        """
            Update the Task instance
        """

        instance.title = validated_data.get('title', instance.title)
        instance.is_done = validated_data.get('is_done', instance.is_done)
        instance.save()

        return instance

    class Meta:
        model = Task
        fields = "__all__"
