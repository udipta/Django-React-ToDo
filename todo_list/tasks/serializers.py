from rest_framework import serializers

from .models import Task


# Task Serializer
class TaskSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        """
            Update the Task instance
        """

        instance.title = validated_data.get('title', instance.title)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created'] = instance.created.isoformat()
        return representation

    class Meta:
        model = Task
        fields = "__all__"
