from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Task(models.Model):
    """
        Task model keeps the information of tasks
        ---
        Contains the definition of Table and it's attributes
    """

    # which user created the entry
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # title of the task
    title = models.CharField(max_length=200)
    # is_done is to keep the information of completion
    is_done = models.BooleanField(default=False)
    # when the entry was created
    created = models.DateTimeField(auto_now=True)
    # when the entry was modified
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created', '-author')
