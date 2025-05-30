from django.db import models
from django.contrib.auth.models import User

"""
Default Django User Model is enough for Teachers
because Teachers only need to log in and
No special fields for teachers is given
"""

class Student(models.Model):
    """
    student model with following fields
    name : students name
    subject: subscribed subject
    marks: gained score in subject
    created_by: teacher / root user who can login
    """
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    marks = models.IntegerField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name