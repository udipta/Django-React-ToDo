from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.
from user_auth.authentication import UserTokenAuthentication
from .models import Task
from .pagination import CustomPageNumberPagination
from .serializers import TaskSerializer


class TaskPagination(CustomPageNumberPagination):
    page_size = 10
    max_page_size = 50


class TaskViewSet(viewsets.ModelViewSet):
    """
        Viewset to create/update/list the Task object.
        **Context**
        :class:`tasks.models.`Task` .

        **Permission** : IsAuthenticated

        :create:
            create the Task object of the given title
        :update:
            update the Task object of the given title
        :list:
            list of Task validated_data for that specific user
    """

    authentication_classes = (UserTokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    pagination_class = TaskPagination

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
            Create task that is specific to the user
            ---
            parameters:
                - name: title
                  required: true
        """
        serializer = self.get_serializer(data=request.data, many=False)
        if serializer.is_valid():
            # set author for Task
            # serializer.validated_data["author"] = request.user
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
            Update title, status for a task.
            ---
            parameters:
                - name: title
                  required: True
                - name: status
                  required: False
        """
        # Partial update
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, many=False, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_304_NOT_MODIFIED)

    @transaction.atomic
    def list(self, request, *args, **kwargs):
        """
            Return a list of Task that is specific to the user
        """
        data = Task.objects.filter(author=request.user).order_by('-id')

        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid()

        # paginate response
        paginated_queryset = self.paginate_queryset(serializer.data)
        paginated_response = self.get_paginated_response(paginated_queryset)

        return Response(paginated_response.data, status=status.HTTP_200_OK)
