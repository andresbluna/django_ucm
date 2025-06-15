import uuid

from django.db import models

class Evaluation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #id = models.CharField(primary_key=True, max_length=100)
    student_id = models.CharField(max_length=100)
    course_id = models.CharField(max_length=100)
    evaluation_name = models.CharField(max_length=255)
    evaluation_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.evaluation_name} ({self.course_id})"



class File(models.Model):
    course_id = models.CharField(max_length=100)
    student_id = models.CharField(max_length=100)
    file_id = models.CharField(max_length=100)
    filename = models.CharField(max_length=255)
    aws_id = models.CharField(max_length=100)
    url = models.URLField()
    mimetype = models.CharField(max_length=100)
    size = models.IntegerField()
    upload_date = models.DateTimeField()

    def __str__(self):
        return f"{self.filename} ({self.course_id} - {self.student_id})"