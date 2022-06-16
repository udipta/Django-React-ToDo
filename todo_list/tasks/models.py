from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Task(models.Model):
    """
        Task model keeps the information of tasks
        ---
        Contains the definition of Table and it's attributes
    """

    TODO = 0
    IN_PROGRESS = 1
    COMPLETED = 2
    STATE_CHOICES = (
        (TODO, 'to-do'),
        (IN_PROGRESS, 'in-progress'),
        (COMPLETED, 'completed')
    )

    # which user created the entry
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # title of the task
    title = models.CharField(max_length=200)
    # status is to keep the information of completion
    status = models.IntegerField(choices=STATE_CHOICES, default=TODO)
    # when the entry was created
    created = models.DateField(auto_now=True)
    # when the entry was modified
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created', '-author')
